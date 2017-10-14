from server import app
from telegram_bot_core import updater


if __name__ == '__main__':
    updater.start_polling()
    app.run(host='0.0.0.0', debug=True)