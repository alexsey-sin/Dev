from telegram import Bot
import os
from dotenv import load_dotenv 
load_dotenv()

bot = Bot(token=os.getenv('TOKEN'))
# Отправка сообщения
chat_id = 1740645090
text = 'Вам телеграмма! Тетя приезжает завтра.'
bot.send_message(chat_id, text)