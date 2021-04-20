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
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import time
import os
import modules.ilias as Ilias
from modules.bot import Bot
from configparser import ConfigParser
import geckodriver_autoinstaller

# Check if the current version of geckodriver exists
# and if it doesn't exist, download it automatically,
# then add geckodriver to path
geckodriver_autoinstaller.install()

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
    
# Create sticker.csv if it not exists
if not os.path.exists('/bot/data/sticker.csv'):
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
