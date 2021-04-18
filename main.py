#!/usr/bin/python3
# main.py

# Copyright (c) 2021, Steven Bruck

import time
import os
import modules.ilias as Ilias
from modules.bot import Bot
from configparser import ConfigParser

# check for existing config
if os.path.exists('/bot/data/config.txt'):
    config = ConfigParser()
    config.read_file(open(r'data/config.txt'))

    # Load general config
    filename = config.get('General', 'filename')
    interval = int(config.get('General', 'update'))

    # Load bot config
    token = config.get('Telegram', 'token')

    # Load ilias config
    username = config.get('Ilias', 'username')
    pwd = config.get('Ilias', 'password')
    timeout = int(config.get('Ilias', 'timeout'))
    url = config.get('Ilias', 'url')
    step1 = config.get('Ilias', 'step1')
    step2 = config.get('Ilias', 'step2')
else:
    print("No config found")
    exit(1)

# Create users.csv if it not exists
if not os.path.exists('/bot/data/users.csv'):
    open('/bot/data/users.csv', mode='w')

#   Ilias Instance
ilias = Ilias.Schedule(username, pwd, filename, timeout, url, step1, step2)

#   Bot Instance
b = Bot(token, filename)

# call update() at specific interval and send update if available
while True:
    if ilias.update():
        b.send_schedule()
    time.sleep(interval)
