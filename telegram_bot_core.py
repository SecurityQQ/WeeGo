
import database
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
#
#
def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

import re


def extract_place(text):
    res = re.findall('го в (\w*)', text.lower())
    if len(res) > 0:
        return res[0]
    else:
        assert False

def echo(bot, update):
    print(update.message.text)
    print('finding place')
    place = extract_place(update.message.text)
    print(place)
    bot.send_message(chat_id=update.message.chat_id, text="ЧУВАКИ, {} РЕАЛЬНО ЗОВЕТ ВАС В {}".format(update.message.from_user.first_name, place) + " Охуенно, сходите, потусуетесь, погнали!")
    database.add_new_activity(update.message.from_user.first_name, place)

def is_triggger(text):
    res = re.findall('го в ([a-zA-Z]*)', text.lower())
    return len(res) > 0


class PlaceFilter(BaseFilter):

    def filter(self, message):
        return bool(message.text and not message.text.startswith('/') and is_triggger(message.text))

placeFilter = PlaceFilter()


updater = Updater('434073103:AAFlPzUSW6ZBMEGPhdjk9W7n0wkdvPlg2eA')


echo_handler = MessageHandler(placeFilter, echo)

updater.dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))