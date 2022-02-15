import os
import time
from datetime import datetime
import requests  # pip install requests

from beeline2 import run_beeline2


# личный бот @infra
# TELEGRAM_CHAT_ID = '1740645090'
# TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot
TELEGRAM_CHAT_ID = '-1001646764735'
TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'


# PERIOD_SCAN = 1 * 60 * 60  # в секундах (1 час)
# PERIOD_BETWEEN = 60
PERIOD_SCAN = 30  # в секундах
PERIOD_BETWEEN = 3


def send_telegram(text: str):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text
        })
    except:
        return 600
    return r.status_code

def write_log(buff, prefix):
    if not os.path.exists('log/'):
        os.mkdir('log/')

    now = datetime.now()
    filename = now.strftime(f'log/{prefix}_%H-%M_%d-%m-%Y.txt')

    with open(filename, 'w', encoding='utf-8') as outfile:
        outfile.write(buff)

def make_report(rez, opsos):
    tlg_mess = ''
    if rez['result'] == 1:  # заявка успешно создана
        tlg_mess = f'{opsos}: - создана заявка\n'
        data = rez.get('data')
        if data:
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Заявка: {data.get("bid_number")}\n'
        send_telegram(tlg_mess)
        print(tlg_mess)
        return
        
    if rez['result'] == 2:  # Ошибка при загрузке заявок из domconnect.ru
        tlg_mess = f'{opsos}:\n'
        comment = rez.get("comment")
        if comment:
            tlg_mess += f'{comment}\n'
        data = rez.get('data')
        if data:
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'ФИО: {data.get("contact_name")}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        send_telegram(tlg_mess)
        print(tlg_mess)
        return
    cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    print(f'{cur_time} {opsos}: Заявок нет')

if __name__ == '__main__':
    # run_beeline2()
    
    # exit()
    
    
    while True:
        start_time = datetime.now()
        #===============================================#
        if start_time.hour >= 6 and start_time.hour < 23:
            # start beeline
            rez = run_beeline2()
            make_report(rez, 'beeline2')
      
        time.sleep(PERIOD_BETWEEN)
        #===============================================#
        
        cur_time = datetime.now()
        passed = (cur_time - start_time).seconds
        left = PERIOD_SCAN - passed
        if left > 0:
            time.sleep(left)
    #####################################################


