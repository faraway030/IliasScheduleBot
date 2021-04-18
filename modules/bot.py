#!/usr/bin/python3
# bot.py

# Copyright (c) 2021, Steven Bruck

import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import csv
import os


class Bot(object):
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
        #   Config
        self.token = token
        self.filename = filename
        self.appdir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
        self.file = self.appdir + "/data/" + filename
        self.users = self.appdir + "/data/users.csv"

        # Handler
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        # Instances
        self.bot = telegram.Bot(self.token)

        # Load stickers
        self.load_sticker()

        #  Logger
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger("BOT")

        # Start the bot
        self.start()

    def load_sticker(self):
        # used keys:
        #   - welcome
        #   - attention
        self.sticker = {}
        with open(self.appdir + "/data/sticker.csv", mode="r") as csvfile:
            reader = csv.reader(csvfile, delimiter="=")
            for line in reader:
                if not line[0] == "":
                    self.sticker[line[0]] = line[1]

    def h_start(self, update, context):
        user = update.message.from_user

        # Check if user already exists
        with open(self.users, mode="r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            exists = 0
            for line in reader:
                if line:
                    if line[1] == str(user.id):
                        exists = 1

        # Add user if not exists
        if exists == 0:
            with open(self.users, mode='a+') as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([user.name, user.id])

                # Logentry
                self.logger.info('New user ' + user.name +
                                 " with ID " + str(user.id))

        # Send welcome message
        self.bot.send_sticker(
            chat_id=update.effective_chat.id, sticker=self.sticker['welcome'])
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.Msg.welcome % (user.name))
        with open(self.file, "rb") as file:
            context.bot.send_document(
                chat_id=update.effective_chat.id, document=file, filename=self.filename)

    def h_echo(self, update, context):
        user = update.message.from_user

        # Logentry
        self.logger.info(user.name + " sent a message: " + update.message.text)

        # Answer to message
        context.bot.send_message(
            chat_id=update.effective_chat.id, text=self.Msg.cantanswer)

    def start(self):
        # Start handler
        self.echo_handler = MessageHandler(
            Filters.text & (~Filters.command), self.h_echo)
        self.start_handler = CommandHandler('start', self.h_start)
        self.dispatcher.add_handler(self.echo_handler)
        self.dispatcher.add_handler(self.start_handler)

        # Start polling
        try:
            self.updater.start_polling()
        except Exception as e:
            self.logger.error(e)

    def send_schedule(self):
        with open(self.users, mode="r") as csvfile:
            users = csv.reader(csvfile, delimiter=';')

            for user in users:
                uname = user[0]
                uid = user[1]

                # Send messages
                try:
                    self.bot.send_sticker(
                        chat_id=uid, sticker=self.sticker['attention'])
                    self.bot.send_message(chat_id=uid, text=self.Msg.update)
                    with open(self.file, "rb") as file:
                        self.bot.sendDocument(
                            chat_id=uid, document=file, filename=self.filename)

                    # Logentry
                    self.logger.info("... sent to: " + uid + " / " + uname)

                # Delete user from csv-file when user has stopped the bot
                except telegram.error.Unauthorized as e:
                    # read file into buffer, except user to delete
                    buf = {}
                    with open(self.users, mode='r') as csvfile:
                        reader = csv.reader(csvfile, delimiter=";")
                        for line in reader:
                            if not user[1] == line[1]:
                                buf[line[1]] = line[0]

                    # write buffer to file
                    with open(self.users, mode='w') as csvfile:
                        writer = csv.writer(
                            csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        for _id, name in buf:
                            writer.writerow([name, _id])

                except telegram.TelegramError as e:
                    self.logger.error(e + " -> " + uid + " / " + uname)
