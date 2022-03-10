import os
import time
from datetime import datetime
import requests  # pip install requests
import json


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

# личный бот @infra
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'


def send_telegram(chat: str, token: str, text: str):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try: requests.post(url, data={'chat_id': chat, 'text': text})
    except: pass

def get_bots_vizit():
    url = url_host + 'api/get_bots_vizit'
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {'key': 'Q8kGM1HfWz'}
    
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        return 1, []
    if responce.status_code == 200:
        bots_vizit = json.loads(responce.text)
        return 0, bots_vizit
    return 2, []

if __name__ == '__main__':
    cur_time = datetime.now()
    # Рабочее время ботов с 6 до 23
    if cur_time.hour < 7 or cur_time.hour >= 23: exit(0)
    
    # Запросим данные о последних посещениях ботов
    e, lst_bots = get_bots_vizit()
    if e: exit(e)
    
    lst_mess = []
    for bot in lst_bots:
        check = bot.get('check')
        if check and check == False: continue 
        name = bot.get('name')
        last_visit = bot.get('last_visit')
        omission = bot.get('omission_min')
        if last_visit == None or last_visit == None or omission == None: continue
        try:
            lv = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S.%f')
            dur_min = int((cur_time - lv).total_seconds() // 60)
            om = int(omission)
            if dur_min > om:
                dur_hour = round(dur_min / 60, 1)
                lst_mess.append(f'{name}: not working {dur_hour} hours.')
        except: pass
    if lst_mess:
        mess = '\n'.join(lst_mess)
        send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
    
    '''
        Запускаем бота через cron
    
        crontab -e    (редактор vi задача будет от имени тек. пользователя (alex))
        Каждый час
        0 */1 * * * cd /var/www/bots && /var/www/bots/venv/bin/python /var/www/bots/check_bots.py
    
    '''
        



