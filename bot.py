import os
import psycopg2
from telegram.ext import Updater, CommandHandler

DATABASE_URL = os.environ.get('DATABASE_URL')
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
PORT = int(os.environ.get('PORT', '8443'))
BASE_CHAT_ID = os.environ['BASE_CHAT_ID']
HEROKU_PROJECT_NAME = os.environ.get('HEROKU_PROJECT_NAME')
IS_LOCAL_DEVELOPMENT = os.environ.get('LOCAL', False)
ADMINISTRATORS = [int(user_id) for user_id in os.environ.get('ADMINISTRATORS').split(',')]

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
conn.autocommit = True
cur = conn.cursor()


def start_handler(bot, update):
    print(bot, update)
    update.message.reply_text('Hi!')
    if update.message.chat.id in ADMINISTRATORS:
        update.message.reply_text('You are administrator!')
    else:
        update.message.reply_text('You aren\'t administrator!')


def get_promos_handler(bot, update):
    return


def get_chats_handler(bot, update):
    return


def main():
    updater = Updater(TELEGRAM_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_handler))
    dp.add_handler(CommandHandler("getPromos", get_promos_handler))
    dp.add_handler(CommandHandler("getChats", get_chats_handler))

    if IS_LOCAL_DEVELOPMENT:
        updater.start_polling()
    else:
        updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TELEGRAM_TOKEN)
        updater.bot.set_webhook("https://%s.herokuapp.com/%s" % (HEROKU_PROJECT_NAME, TELEGRAM_TOKEN))

    print('Started')

    updater.idle()


if __name__ == '__main__':
    main()
