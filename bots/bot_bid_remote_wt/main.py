import os
import time
from datetime import datetime
import requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By

from lk_megafon import run_lk_megafon
from lk_beeline import run_lk_beeline
from bid_beeline import run_bid_beeline
from bid_rostelecom2 import run_bid_rostelecom2
from bid_rostelecom import run_bid_rostelecom
from bid_mts import run_bid_mts
from bid_domru import run_bid_domru
from bid_ttk import run_bid_ttk
from bid_onlime import run_bid_onlime

# личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot Парсинг ЛК       LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN
LK_TELEGRAM_CHAT_ID = '-1001580291081'
LK_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

# общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
BID_TELEGRAM_CHAT_ID = '-1001646764735'
BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

TIME_1_HOUR = 1 * 60 * 60  # в секундах
TIME_30_SECONDS = 30  # в секундах, 

PERIOD_SCAN_BID_BEELINE = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок BEELINE
PERIOD_SCAN_BID_MTS = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок MTS
PERIOD_SCAN_BID_ROSTELECOM2 = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок ROSTELECOM2
PERIOD_SCAN_BID_ROSTELECOM = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок ROSTELECOM
PERIOD_SCAN_BID_DOMRU = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок DOMRU
PERIOD_SCAN_BID_TTK = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок TTK
PERIOD_SCAN_BID_ONLIME = TIME_30_SECONDS  # Периодичность работы скрипта заведение заявок ONLIME
PERIOD_SCAN_LK_MEGAFON = TIME_1_HOUR  # Периодичность работы парсинг ЛК MEGAFON
PERIOD_SCAN_LK_BEELINE = TIME_1_HOUR  # Периодичность работы парсинг ЛК BEELINE
PERIOD_BETWEEN = 1  # в секундах, Пауза

def send_telegram(chat: str, token: str, text: str):
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
    # print(resp.status_code)
    # print(resp.text)

# def write_log(buff, prefix):
    # if not os.path.exists('log/'):
        # os.mkdir('log/')

    # now = datetime.now()
    # filename = now.strftime(f'log/{prefix}_%H-%M_%d-%m-%Y.txt')

    # with open(filename, 'w', encoding='utf-8') as outfile:
        # outfile.write(buff)

def make_lk_report(rez, opsos):
    tlg_mess = 'not message'
    if rez[0]:  # если ошибка
        tlg_mess = f'Parsing {opsos} - ERROR: {rez[0]}'
        print(tlg_mess)
    else:  # если всё хорошо
        print(f'Parsing {opsos} is OK. See logs')
        print(rez[2])
        send_api(rez[1])
        # write_log(rez[3], opsos)
        tlg_mess = rez[3]
    ans = send_telegram(LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN, tlg_mess)
    s_ans = 'OK'
    if ans != 200:
        s_ans = str(ans)
    print('Send TELEGRAMM:', s_ans)


if __name__ == '__main__':
    start_time_bid_beeline = None
    start_time_bid_mts = None
    start_time_bid_rostelecom2 = None
    start_time_bid_rostelecom = None
    start_time_bid_domru = None
    start_time_bid_ttk = None
    start_time_bid_onlime = None
    start_time_lk_megafon = None
    start_time_lk_beeline = None
    
    while True:
        time.sleep(PERIOD_BETWEEN)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        str_time = cur_time.strftime('%H:%M:%S %d-%m-%Y')
        
        # #===============================================#
        # # Скрипт Заведение заявок beeline
        # if start_time_bid_beeline:
            # passed = (cur_time - start_time_bid_beeline).seconds
        # if start_time_bid_beeline == None or passed >= PERIOD_SCAN_BID_BEELINE:
            # start_time_bid_beeline = cur_time
            # print(f'start bid_beeline {str_time}')
            # # run_bid_beeline(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_bid_beeline(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Заведение заявок mts
        # if start_time_bid_mts:
            # passed = (cur_time - start_time_bid_mts).seconds
        # if start_time_bid_mts == None or passed >= PERIOD_SCAN_BID_MTS:
            # start_time_bid_mts = cur_time
            # print(f'start bid_mts {str_time}')
            # run_bid_mts(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Заведение заявок rostelecom2
        # if start_time_bid_rostelecom2:
            # passed = (cur_time - start_time_bid_rostelecom2).seconds
        # if start_time_bid_rostelecom2 == None or passed >= PERIOD_SCAN_BID_ROSTELECOM2:
            # start_time_bid_rostelecom2 = cur_time
            # print(f'start bid_rostelecom2 {str_time}')
            # run_bid_rostelecom2(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Заведение заявок rostelecom
        # if start_time_bid_rostelecom:
            # passed = (cur_time - start_time_bid_rostelecom).seconds
        # if start_time_bid_rostelecom == None or passed >= PERIOD_SCAN_BID_ROSTELECOM:
            # start_time_bid_rostelecom = cur_time
            # print(f'start bid_rostelecom {str_time}')
            # run_bid_rostelecom(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Заведение заявок domru
        # if start_time_bid_domru:
            # passed = (cur_time - start_time_bid_domru).seconds
        # if start_time_bid_domru == None or passed >= PERIOD_SCAN_BID_DOMRU:
            # start_time_bid_domru = cur_time
            # print(f'start bid_domru {str_time}')
            # run_bid_domru(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Заведение заявок ttk
        # if start_time_bid_ttk:
            # passed = (cur_time - start_time_bid_ttk).seconds
        # if start_time_bid_ttk == None or passed >= PERIOD_SCAN_BID_TTK:
            # start_time_bid_ttk = cur_time
            # print(f'start bid_ttk {str_time}')
            # run_bid_ttk(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # continue

        #===============================================#
        # Скрипт Заведение заявок onlime
        if start_time_bid_onlime:
            passed = (cur_time - start_time_bid_onlime).seconds
        if start_time_bid_onlime == None or passed >= PERIOD_SCAN_BID_ONLIME:
            start_time_bid_onlime = cur_time
            print(f'start bid_onlime {str_time}')
            # run_bid_onlime(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            run_bid_onlime(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        # #===============================================#
        # # Скрипт парсинг ЛК megafon
        # if start_time_lk_megafon:
            # passed = (cur_time - start_time_lk_megafon).seconds
        # if start_time_lk_megafon == None or passed >= PERIOD_SCAN_LK_MEGAFON:
            # start_time_lk_megafon = cur_time
            # print(f'start lk_megafon {str_time}')
            # rez = run_lk_megafon()
            # make_lk_report(rez, 'megafon')
            # continue

        # #===============================================#
        # # Скрипт парсинг ЛК beeline
        # if start_time_lk_beeline:
            # passed = (cur_time - start_time_lk_beeline).seconds
        # if start_time_lk_beeline == None or passed >= PERIOD_SCAN_LK_BEELINE:
            # start_time_lk_beeline = cur_time
            # print(f'start lk_beeline {str_time}')
            # rez = run_lk_beeline()
            # make_lk_report(rez, 'beeline')
            # continue

    #####################################################
