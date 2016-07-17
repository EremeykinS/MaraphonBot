from config import *
from wit import Wit
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import telegram

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('Maraphon_test_bot.' + __name__)

# dict in dict
dd = dict()

# Keyboards
main_kbd = telegram.ReplyKeyboardMarkup([['Категории', 'О марафонах'], ['Моя программа', 'INFO']])
yes_no_kbd = telegram.ReplyKeyboardMarkup([['Да'], ['Нет']])
empty_kbd = telegram.ReplyKeyboardHide()


def start(bot, update):
    text = "Добро пожаловать в MyMaraphon! Здесь вы можете задать любой вопрос о подготовке и проведении марафонов. Воспользуйтесь меню, или просто введите интересующий вас вопрос самостоятельно"
    bot.sendMessage(update.message.chat_id, text=text, reply_markup=main_kbd)


def helper(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def chat(bot, update):
    user_id = update.message.from_user.id
    answer = update.message.text

    if answer == 'О марафонах':
        text = "Марафоны - это круто!"
        bot.sendMessage(user_id, text=text, reply_markup=main_kbd)     
    elif answer == 'Категории':
        text = "Пока категории вопросов не созданы. Вы можете ввести вопрос самостоятельно"
        bot.sendMessage(user_id, text=text, reply_markup=main_kbd)
    elif answer == 'Моя программа':
        text = "Подождите, какая нахуй программа? Вы же даже не знаете, что такое марафон. Сначала узнайте, а потом уже приходите"
        bot.sendMessage(user_id, text=text, reply_markup=main_kbd)
    elif answer == 'INFO':
        text = "Появление информации ожидается в скором времени"
        bot.sendMessage(user_id, text=text, reply_markup=main_kbd)
    else:
        actions = dict()
        client = Wit(access_token=wit_token, actions=actions)
        client_answer = client.message(answer)
        if client_answer['entities']['intent'][0]['confidence'] < 0.6:
            text = "К сожалению, ответ на этот вопрос мне не известен. Попробуйте другой вопрос."
            bot.sendMessage(user_id, text=text, reply_markup=main_kbd)
        else:
            codec = client_answer['entities']['intent'][0]['value']
            text = dictionary[codec]
            bot.sendMessage(user_id, text=text, reply_markup=main_kbd)
        

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(telegram_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", helper))

    # on noncommand i.e message
    dp.add_handler(MessageHandler([Filters.text], chat))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen='95.163.114.6', # 95.163.114.6
                      port=80,
                      url_path='MaraphonBot',
                      key='/home/user/cert/private.key',
                      cert='/home/user/cert/cert.pem',
                      webhook_url='https://95.163.114.6:80/MaraphonBot')
    updater.idle()


if __name__ == '__main__':
    main()
