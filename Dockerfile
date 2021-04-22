FROM ubuntu:latest
LABEL maintainer="Steven Bruck dev@bruck.xyz" \
      version="1.2"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Berlin

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install requirements
COPY requirements.txt .
RUN apt update && \
    apt install --no-install-recommends --no-install-suggests firefox firefox-geckodriver python3 python3-pip tzdata -y && \
    python3 -m pip install --upgrade pip && \
    python3 -m pip install -r requirements.txt && \
    rm requirements.txt

# Set timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    dpkg-reconfigure --frontend noninteractive tzdata

WORKDIR /bot
COPY main.py .
COPY backend/handler.py backend/
COPY backend/ilias.py backend/

ENTRYPOINT ["python3", "main.py"]