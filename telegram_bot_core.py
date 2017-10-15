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
from get_airplane_tickets import getTickets
import re

import geotaging

def start(bot, update):
    update.message.reply_text('Hello World!')


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def is_triggger(text):
    res = recogniseEvent(text)
    return len(res) > 0

def extract_place(text):
    return recogniseEvent(text)

def echo(bot, update):
    event = extract_place(update.message.text)
    event_where = event['where'][0] if len(event['where']) > 0 else ''
    event_when = event['when'][0] if len(event['when']) > 0 else ''
    event_what = event['what'][0] if len(event['what']) > 0 else event_where
    print(event_what + ' - ' + event_where + ' - ' + event_when)

    if event_what:
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('like', callback_data='like'),
                                              InlineKeyboardButton('dislike', callback_data='dislike')]])
        bot_msg = bot.send_message(chat_id=update.message.chat_id, reply_markup=reply_markup, parse_mode='markdown',
                         text="Guys, [{}](tg://user?id={}) invites you to {}{}. Wonderful idea, let's go!".format(
                             update.message.from_user.first_name,
                             update.message.from_user.id,
                             event_what,
                             ' ' + event_when if event_when != '' else ''
                         ))
        name = update.message.from_user.first_name + ' ' + update.message.from_user.last_name
        activity_id = database.add_new_activity(
            event_what, event_where, event_when, update.message.text, update.message.from_user.id, name, update.message.from_user.name)
        database.add_like(activity_id, update.message.from_user.id, name, update.message.from_user.name)
        database.update_activity(activity_id, bot_msg.chat_id, bot_msg.message_id)



class PlaceFilter(BaseFilter):
    def filter(self, message):
        return bool(message.text and not message.text.startswith('/') and is_triggger(message.text))


placeFilter = PlaceFilter()


def button(bot, update):
    query = update.callback_query

    try:
        activity = database.get_activity_by_msg(query.message.chat_id, query.message.message_id)

        user_name = query.from_user.first_name + ' ' + query.from_user.last_name
        if query.data == 'like':
            database.add_like(activity['id'], query.from_user.id, user_name, query.from_user.name)
            database.remove_dislike(activity['id'], query.from_user.id)
        else:
            database.add_dislike(activity['id'], query.from_user.id, user_name, query.from_user.name)
            database.remove_like(activity['id'], query.from_user.id)

        text="Guys, [{}](tg://user?id={}) invites you to {}{}. Wonderful idea, let's go!".format(
            activity['author_name'].split()[0],
            activity['author'],
            activity['title'],
            ' on ' + activity['event_when'] if activity['event_when'] != '' else ''
        )

        likes_list = database.get_likes(activity['id'])
        likes = ['[{0}](tg://user?id={1})'.format(x['person_name'], x['person']) for x in likes_list]
        dislikes = ['[{0}](tg://user?id={1})'.format(x['person_name'], x['person']) for x in database.get_dislikes(activity['id'])]
        text += '\n—\n👍 {0}\n—\n👎 {1}'.format(', '.join(likes), ', '.join(dislikes))

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton('like', callback_data='like'), InlineKeyboardButton('dislike', callback_data='dislike')]])

        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=reply_markup,
                              parse_mode='markdown')

        if len(likes_list) >= 3 and activity['title'] in ['cinema', 'theatre'] and database.check_invoice(activity['id']):
            database.send_invoice(activity['id'])

            translate = {
                'cinema': 'sinema',
                'theatre': 'teatro'
            }
            nearest = geotaging.get_places_nearby(radius=1000, name=translate[activity['title']])[0]

            try:
                for user in likes_list:
                    buy2(bot, update, activity, user, nearest['vicinity'], 'qr-code')
            except Exception as e:
                print(e)

            bot.send_message(
                chat_id=query.message.chat_id,
                parse_mode='markdown',
                text="Ok, we go to the {0} ({1}), switch to @WeeGoBot for payment".format(nearest['name'], activity['title']))
            bot.send_location(chat_id=query.message.chat_id, latitude=nearest['lat'], longitude=nearest['lng'])
        elif len(likes_list) >= 3 and activity['title'] == activity['event_where'] and database.check_invoice(activity['id']):
            database.send_invoice(activity['id'])
            try:
                quote_best = getTickets(activity['title'])
                bot.send_message(
                    chat_id=query.message.chat_id,
                    parse_mode='markdown',
                    text="The cheapest variant to go to {}: {} from {} USD".format(
                        activity['title'],
                        quote_best['OutboundLeg']['DepartureDate'][0:10],
                        quote_best['MinPrice']))
                bot.send_document(chat_id=query.message.chat_id, document=quote_best['Url'])
            except Exception as e:
                pass

    except Exception as e:
        print(e)
        raise
    query.answer()


# updater = Updater('434073103:AAFlPzUSW6ZBMEGPhdjk9W7n0wkdvPlg2eA')
updater = Updater('471069982:AAFps0N56HO1RCCMidRpqcd2OtFT8HzQdJ0')

echo_handler = MessageHandler(placeFilter, echo)

updater.dispatcher.add_handler(echo_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))


def precheckout_callback(bot, update):
    query = update.pre_checkout_query
    if query.invoice_payload.startswith('qr-code') or query.invoice_payload.startswith('no-qr-code'):
        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)
    #     print(res)
    else:
        return
    #

def successful_payment_callback(bot, update):
    update.message.reply_text("Have a nice evening!")
    payload = update.message.successful_payment.invoice_payload
    print(payload)
    payload, title = payload.split('Z')
    if payload == 'qr-code':
        bot.send_photo(update.message.from_user.id,
                       photo=open('./{0}.png'.format(title), 'rb'),
                       caption="It is your ticket, scan it in the " + title)


def buy2(bot, update, activity, user, vicinity, payload):
    title = activity['title']

    prices_dict = {
        'cinema': 799,
        'theatre': 2499
    }

    prices = [LabeledPrice(title.capitalize() + ' Ticket', prices_dict[title])]
    title = title.capitalize() + ' Ticket'
    description = 'Address: ' + vicinity
    start_parameter = 'start_parameter'
    currency = 'EUR'

    bot.send_message(chat_id=user['person'], text="Tickets receipt")

    bot.send_invoice(user['person'],
                     title,
                     description,
                     payload + 'Z' + activity['title'],
                     provider_token="284685063:TEST:MzYxZDFhMjNjNTVj",
                     start_parameter=start_parameter,
                     currency=currency,
                     prices=prices)


def buy(bot, update, payload):
    prices = [LabeledPrice('Cinema Ticket', 799)]
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
                     prices=prices)

def send_invoice_with_qr_code_hook(bot, update):
    return buy(bot, update, 'qr-code')

def send_invoice_no_qr_code(bot, update):
    return buy(bot, update, 'no-qr-code')


updater.dispatcher.add_handler(CommandHandler('buy_with_qr', send_invoice_with_qr_code_hook))
updater.dispatcher.add_handler(CommandHandler('buy_no_qr', send_invoice_no_qr_code))

updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
updater.dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
