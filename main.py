#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import os
import sys
from uuid import uuid4

from PIL import Image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def photo(bot, update):
    image = update.message.photo[-1]
    file_id = image.file_id
    newFile = bot.get_file(file_id)
    file_name = "{}.png".format(uuid4())
    newFile.download(file_name)
    imbg = Image.open(file_name)
    imfg = Image.open("23.png")
    imbg_width, imbg_height = imbg.size
    imfg_resized = imfg.resize((imbg_width, imbg_height), Image.LANCZOS)
    imbg.paste(imfg_resized, None, imfg_resized)
    imbg.save("overlay.png")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('overlay.png', 'rb'))


def error(bot, update):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main():
    try:
        token = sys.argv[1]
    except IndexError:
        token = os.environ.get("TOKEN")
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.photo, photo))
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Ready to rock..!")
    updater.idle()


if __name__ == '__main__':
    main()
