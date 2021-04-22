#!/usr/bin/python3
# main.py

'''
Copyright (C) 2021  Steven Bruck

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.c
'''

import time
import os
from backend.ilias import Ilias
from configparser import ConfigParser

# check for existing config
if os.path.exists('data/config.txt'):
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
if not os.path.exists('data/users.csv'):
    open('data/users.csv', mode='w')

# Create sticker.csv if it not exists
if not os.path.exists('data/sticker.csv'):
    open('data/users.csv', mode='w')

#   Bot Instance
bot = Ilias(token, username, pwd, filename, timeout, url, step1, step2)

# call update() at specific interval and send update if available
while True:
    if bot.update():
        bot.send_schedule()
    time.sleep(interval)
