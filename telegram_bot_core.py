
import database
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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


# def like_callback(id, from_user, message)


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

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('like', callback_data='like'), InlineKeyboardButton('dislike', callback_data='dislike')]])
    bot_msg = bot.send_message(chat_id=update.message.chat_id, reply_markup=reply_markup, text="ЧУВАКИ, {} РЕАЛЬНО ЗОВЕТ ВАС В {}".format(
        update.message.from_user.first_name, place) + ". Охуенно, сходите, потусуетесь, погнали!")
    database.update_activity(activity_id, bot_msg.chat_id, bot_msg.message_id)


def is_triggger(text):
    res = re.findall('го в ([a-zA-Z]*)', text.lower())
    return len(res) > 0


class PlaceFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text and not message.text.startswith('/') and is_triggger(message.text))


class LikeFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text and not message.text.startswith('/') and (message.text == 'like' or message.text == 'go') and 
            message.reply_to_message and message.reply_to_message.text.startswith('ЧУВАКИ, ') and message.reply_to_message.to_dict()['from']['is_bot'])


def echo_like(bot, update):
    print(update.message.text)
    print('finding place')
    id_ = int(update.message.reply_to_message.text.rsplit(' ', 1)[-1])
    place = database.get_activity_by_id(id_)['title']
    bot.send_message(chat_id=update.message.chat_id, 
        text="ЧУВАКИ, {} ТОЖЕ ХОЧЕТ СГОНЯТЬ В {}".format(
        update.message.from_user.first_name, place) + ". Нужно идти, инфа соточка!")
    name = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
    database.add_like(id_, update.message.from_user.id, name)


placeFilter = PlaceFilter()


def button(bot, update):
    query = update.callback_query

    activity = database.get_activity_by_msg(query.message.chat_id, query.message.message_id)

    user_name = query.from_user.first_name + ' ' + query.from_user.last_name
    if query.data == 'like':
        database.add_like(activity['id'], query.from_user.id, user_name)
        database.remove_dislike(activity['id'], query.from_user.id)
    else:
        database.add_dislike(activity['id'], query.from_user.id, user_name)
        database.remove_like(activity['id'], query.from_user.id)


    likes = [x['person_name'] for x in database.get_likes(activity['id'])]
    dislikes = [x['person_name'] for x in database.get_dislikes(activity['id'])]
    text = 'Норм идея: {0}\nНеоч: {1}'.format(', '.join(likes), ', '.join(dislikes))

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('like', callback_data='like'), InlineKeyboardButton('dislike', callback_data='dislike')]])

    bot.edit_message_text(text=text,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          reply_markup=reply_markup)

    query.answer()


# updater = Updater('434073103:AAFlPzUSW6ZBMEGPhdjk9W7n0wkdvPlg2eA')
updater = Updater('471069982:AAFps0N56HO1RCCMidRpqcd2OtFT8HzQdJ0')

echo_handler = MessageHandler(placeFilter, echo)
like_handler = MessageHandler(LikeFilter(), echo_like)

updater.dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(like_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))