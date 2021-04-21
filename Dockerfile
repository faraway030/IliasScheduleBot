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
RUN apk update && \
    apk add --no-cache firefox-esr tzdata && \
    python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt && \
    rm requirements.txt

WORKDIR /bot
COPY main.py /bot/
COPY modules/bot.py /bot/modules/
COPY modules/ilias.py /bot/modules/

ENTRYPOINT ["python", "main.py"]