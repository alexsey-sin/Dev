import os
import time
from datetime import datetime
import requests  # pip install requests

from mts import run_mts

# личный бот Синицин А.С. @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot
WORK_TELEGRAM_CHAT_ID = '-1001580291081'
WORK_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'



PERIOD_SCAN = 1 * 60 * 60  # в секундах (1 час)
PERIOD_BETWEEN = 60
# PERIOD_SCAN = 600  # в секундах
# PERIOD_BETWEEN = 3

def send_telegram(chat, token, text):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": chat,
            "text": text
        })
    except:
        return 600
    return r.status_code

def send_api(data):
    # API_MOBILE_URL = 'http://127.0.0.1:8000/mobile/api'
    # BSE_URL = 'http://127.0.0.1:8000/'

    API_MOBILE_URL = 'http://37.46.128.40/mobile/api'
    BSE_URL = 'http://37.46.128.40/'

    try:
        client = requests.session()
        resp = client.get(BSE_URL)
        csrftoken = resp.cookies.get('csrftoken')
        header = {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken,
        }
        resp = client.post(API_MOBILE_URL, headers=header, json=data)
    except:
        return 1

    return 0

def write_log(buff, prefix):
    if not os.path.exists('log/'):
        os.mkdir('log/')

    now = datetime.now()
    filename = now.strftime(f'log/{prefix}_%H-%M_%d-%m-%Y.txt')

    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(buff)

def make_report(rez, opsos):
    tlg_mess = 'not message'
    if rez[0]:  # если ошибка
        tlg_mess = f'Parsing {opsos} - ERROR: {rez[0]}\n{rez[3]}'
        # print(tlg_mess)
    else:  # если всё хорошо
        # print(f'Parsing {opsos} is OK. See logs')
        # print(rez[2])
        send = send_api(rez[1])
        # write_log(rez[3], opsos)
        tlg_mess = rez[3]
    # ans = send_telegram(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, tlg_mess)
    ans = send_telegram(WORK_TELEGRAM_CHAT_ID, WORK_TELEGRAM_TOKEN, tlg_mess)
    # print(tlg_mess)


if __name__ == '__main__':
    print('start')
    while True:
        start_time = datetime.now()
        #===============================================#
        if start_time.hour >= 6 and start_time.hour < 23:
            # start mts
            rez = run_mts()
            make_report(rez, 'mts')
            
        #===============================================#
        time.sleep(PERIOD_BETWEEN)
        
        
        cur_time = datetime.now()
        passed = (cur_time - start_time).seconds
        left = PERIOD_SCAN - passed
        if left > 0:
            time.sleep(left)
