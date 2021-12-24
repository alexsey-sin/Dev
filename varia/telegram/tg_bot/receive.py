from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import os
import sys
from dotenv import load_dotenv 
load_dotenv()

updater = Updater(token=os.getenv('TOKEN'))

def say_hi(bot, update):
    # В ответ на любое сообщение, переданное в аргумент update, 
    # будет отправлено сообщение 'Привет, я бот'
    bot.message.reply_text('Привет, я super бот')

def wake_up(bot, update):
    # В ответ на команду будет отправлено сообщение 'Спасибо, что включили меня'
    bot.message.reply_text('Спасибо, что включили меня')

def wake_stop(bot, update):
    # В ответ на команду будет отправлено сообщение 'Спасибо, что включили меня'
    bot.message.reply_text('Я выключаюсь!')
    # updater.stop()
    # sys.exit()

# Для обработки команды /start
updater.dispatcher.add_handler(CommandHandler('start', wake_up))
# Для обработки команды /stop
updater.dispatcher.add_handler(CommandHandler('stop', wake_stop))

# Регистрируется обработчик MessageHandler;
# из всех полученных сообщений он будет выбирать только текстовые сообщения
# и передавать их в функцию say_hi()
updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))


# Метод start_polling() запускает процесс polling, 
# приложение начнёт отправлять регулярные запросы для получения обновлений.
updater.start_polling(poll_interval=2.0)  # sec