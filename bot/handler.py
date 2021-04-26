#!/usr/bin/python3
# bot.py

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

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import csv
import os


class BotHandler(telegram.Bot):
    # TODO: Save and load messages from customizable file in /bot/data
    class Msg:
        # predefining messages
        welcome = ("Hallo %s! Darf ich mich vorstellen?\n"
                   "Ich bin Dozentus Informatikus Maximus!\n\n"
                   "Ich werde regelmäßig für dich überprüfen, ob es einen neuen Stundenplan gibt und "
                   "dir diesen hier schicken!"
                   "\n\n"
                   "Aktuell gilt dieser Stundenplan:"
                   )
        update = "Es ist ein neuer Stundenplan verfügbar:"
        cantanswer = "Auf Nachrichten antworten kann ich leider noch nicht."

    def __init__(self, token, filename):
        super(BotHandler, self).__init__(token)

        #   Config
        self.__filename = filename
        self.__appdir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        self.__file = self.__appdir + "/data/" + filename
        self.__users = self.__appdir + "/data/users.csv"

        # Handler
        self.__updater = Updater(token=token, use_context=True)
        self.__dispatcher = self.__updater.dispatcher

        # Load stickers
        self.__load_sticker()

        #  Logger
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("BOT")

        # Start the bot
        self.__start()

    def __load_sticker(self):
        # used keys:
        #   - welcome
        #   - attention
        self.__sticker = {}
        with open(self.__appdir + "/data/sticker.csv", mode="r") as csvfile:
            reader = csv.reader(csvfile, delimiter="=")
            for line in reader:
                if not line[0] == "":
                    self.__sticker[line[0]] = line[1]

    def __h_start(self, update, context):
        user = update.message.from_user

        # Check if user already exists
        with open(self.__users, mode="r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            exists = 0
            for line in reader:
                if line:
                    if line[1] == str(user.id):
                        exists = 1

        # Add user if not exists
        if exists == 0:
            with open(self.__users, mode='a+') as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([user.name, user.id])

                # Logentry
                self.logger.info('New user ' + user.name +
                                 " with ID " + str(user.id))

        # Send welcome message
        self.send_sticker(
            chat_id=update.effective_chat.id, sticker=self.__sticker['welcome'])
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.Msg.welcome % (user.name))
        with open(self.__file, "rb") as file:
            context.bot.send_document(
                chat_id=update.effective_chat.id, document=file, filename=self.__filename)

    def __h_echo(self, update, context):
        user = update.message.from_user

        # Logentry
        self.logger.info(user.name + " sent a message: " + update.message.text)

        # Answer to message
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.Msg.cantanswer)

    def __start(self):
        # Start handler
        self.__echo_handler = MessageHandler(
            Filters.text & (~Filters.command), self.__h_echo)
        self.__start_handler = CommandHandler('start', self.__h_start)
        self.__dispatcher.add_handler(self.__echo_handler)
        self.__dispatcher.add_handler(self.__start_handler)

        # Start polling
        try:
            self.__updater.start_polling()
            self.logger.info("Started")
        except Exception as e:
            self.logger.error(e)

    def send_schedule(self):
        with open(self.__users, mode="r") as csvfile:
            users = csv.reader(csvfile, delimiter=';')

            for user in users:
                uname = user[0]
                uid = user[1]

                # Send messages
                try:
                    print(f'User: {uname} with ID: {uid}')
                    self.send_sticker(chat_id=uid, sticker=self.__sticker['attention'])
                    self.send_message(chat_id=uid, text=self.Msg.update)
                    with open(self.__file, "rb") as file:
                        self.sendDocument(
                            chat_id=uid, document=file, filename=self.__filename)

                    # Logentry
                    self.logger.info("... sent to: " + uid + " / " + uname)

                # Delete user from csv-file when user has stopped the bot
                except telegram.error.Unauthorized as e:
                    # read file into buffer, except user to delete
                    buf = {}
                    with open(self.__users, mode='r') as csvfile:
                        reader = csv.reader(csvfile, delimiter=";")
                        for line in reader:
                            if not user[1] == line[1]:
                                buf[line[1]] = line[0]

                    # write buffer to file
                    with open(self.__users, mode='w') as csvfile:
                        writer = csv.writer(
                            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for _id, name in buf:
                            writer.writerow([name, _id])

                except telegram.TelegramError as e:
                    self.logger.error(e + " -> " + uid + " / " + uname)
