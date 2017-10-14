
import database
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter
from recognise_event import recogniseEvent
import re


def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def extract_place(text):
    result = recogniseEvent(text)
    if len(result['what']) > 0:
        return result
    else:
        assert False

def echo(bot, update):
    print(update.message.text)
    print('finding place')
    event = extract_place(update.message.text)
    event_what = event['what'][0]
    event_where = event['where'][0] if len(event['where']) > 0 else ''
    event_when = event['when'][0] if len(event['when']) > 0 else ''
    print(event_what + ' ' + event_where + ' ' + event_when)
    bot.send_message(chat_id=update.message.chat_id,
                     text="Guys!, {} invites you to {}. Wonderful idea, let's go!".format(
                         update.message.from_user.first_name, event_what))
    name = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
    activity_id = database.add_new_activity(event_what, event_where, event_when, update.message.text, update.message.from_user.id, name)
    database.add_like(activity_id, update.message.from_user.id, name)

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