
import database
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, ShippingQueryHandler, PreCheckoutQueryHandler, Filters
from telegram.invoice import Invoice
from telegram.labeledprice import LabeledPrice
from telegram.successfulpayment import SuccessfulPayment


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
    bot.send_message(chat_id=update.message.chat_id, text="ЧУВАКИ, {} ({}) РЕАЛЬНО ЗОВЕТ ВАС В {}".format(
        update.message.from_user.first_name, update.message.from_user.id, place) + ". Охуенно, сходите, потусуетесь, погнали!")
    print(322)
    activity_id = database.add_new_activity(place, update.message.from_user.id)
    print(1488)
    database.add_like(activity_id, update.message.from_user.id)

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