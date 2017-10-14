import database
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,\
    CommandHandler,\
    MessageHandler,\
    BaseFilter,\
    ShippingQueryHandler,\
    PreCheckoutQueryHandler,\
    Filters,\
    CallbackQueryHandler

from telegram.labeledprice import LabeledPrice
from telegram.successfulpayment import SuccessfulPayment
from recognise_event import recogniseEvent
import re

def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def is_triggger(text):
    res = recogniseEvent(text)
    return len(res) > 0

def extract_place(text):
    result = recogniseEvent(text)
    if len(result['what']) > 0:
        return result
    else:
        return False

def echo(bot, update):
    event = extract_place(update.message.text)
    event_what = event['what'][0]
    event_where = event['where'][0] if len(event['where']) > 0 else ''
    event_when = event['when'][0] if len(event['when']) > 0 else ''
    print(event_what + ' ' + event_where + ' ' + event_when)
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('like', callback_data='like'), InlineKeyboardButton('dislike', callback_data='dislike')]])
    bot_msg = bot.send_message(chat_id=update.message.chat_id, reply_markup=reply_markup,
                     text="Guys!, {} invites you to {}. Wonderful idea, let's go!".format(
                     update.message.from_user.first_name, event_what))
    name = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
    activity_id = database.add_new_activity(event_what, event_where, event_when, update.message.text, update.message.from_user.id, name)
    database.add_like(activity_id, update.message.from_user.id, name)

    database.update_activity(activity_id, bot_msg.chat_id, bot_msg.message_id)



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


def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    if query.invoice_payload == 'qr-code' or query.invoice_payload == 'no-qr-code':
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    #     print(res)
    else:
        return
    #

def successful_payment_callback(bot, update):
    update.message.reply_text("Have a nice evening!")
    payload = update.message.successful_payment.invoice_payload
    print(payload)
    if payload == 'qr-code':
        bot.send_photo(update.message.from_user.id,
                       photo=open('./cinema.png', 'rb'),
                       caption="It is your ticket, scan it in the cinema")

def buy(bot, update, payload):
    prices = [LabeledPrice('Cinema Ticket', 300099)]
    title = 'Cinema Ticket'
    description = 'Diagonal, 11'
    start_parameter = 'start_parameter'
    currency = 'EUR'

    bot.send_message(chat_id=update.message.chat_id, text="Ok, we go to the cinema, switch to @WeeGoBot for payment")
    bot.send_message(chat_id=update.message.from_user.id, text="Tickets receipt")

    bot.send_invoice(update.message.from_user.id,
                     title,
                     description,
                     payload,
                     provider_token="284685063:TEST:MzYxZDFhMjNjNTVj",
                     start_parameter=start_parameter,
                     currency=currency,
                     prices=prices
                     )

def send_invoice_with_qr_code_hook(bot, update):
    return buy(bot, update, 'qr-code')

def send_invoice_no_qr_code(bot, update):
    return buy(bot, update, 'no-qr-code')


updater.dispatcher.add_handler(CommandHandler('buy_with_qr', send_invoice_with_qr_code_hook))
updater.dispatcher.add_handler(CommandHandler('buy_no_qr', send_invoice_no_qr_code))

updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
