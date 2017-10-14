from server import app
from telegram_bot_core import updater
import logging


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.ERROR)
    updater.start_polling()
    app.run(host='0.0.0.0', debug=True)

def qr():
    from MyQR import myqr
    ver, ecl, qr_name = myqr.run("http://cinecapritheater.com", picture='/Developer/PycharmProjects/WhereToGo/33692.png', save_name="cinema.png")