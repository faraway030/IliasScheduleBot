FROM ubuntu:latest

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Berlin

# Install requirements
COPY requirements.txt .
RUN apt update -y && apt upgrade -y
RUN apt install --no-install-recommends --no-install-suggests wget curl bzip2 firefox firefox-geckodriver python3 python3-pip tzdata -y
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN dpkg-reconfigure --frontend noninteractive tzdata
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt


WORKDIR /bot
VOLUME /bot/data/
COPY config_template.txt /bot/data/
COPY main.py /bot/
COPY modules/bot.py /bot/modules/
COPY modules/ilias.py /bot/modules/

CMD ["python3", "main.py"]