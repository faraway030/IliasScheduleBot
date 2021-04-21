FROM python:3.9-alpine
LABEL maintainer="Steven Bruck dev@bruck.xyz" \
      version="1.2"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Berlin

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install requirements
COPY requirements.txt .
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-2.30-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.30-r0/glibc-bin-2.30-r0.apk && \
    apk update && \
    apk add --no-cache firefox-esr tzdata glibc-2.30-r0.apk glibc-bin-2.30-r0.apk && \
    wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz && \
    tar -zxf geckodriver-v0.26.0-linux64.tar.gz -C /usr/bin && \
    geckodriver --version && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt && \
    rm requirements.txt

WORKDIR /bot
COPY main.py /bot/
COPY modules/bot.py /bot/modules/
COPY modules/ilias.py /bot/modules/

ENTRYPOINT ["python", "main.py"]