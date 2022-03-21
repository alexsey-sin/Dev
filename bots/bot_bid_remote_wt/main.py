import os, time, threading
from datetime import datetime, timedelta
# import os
# import time
# from datetime import datetime
# import requests  # pip install requests
# from selenium import webdriver  # $ pip install selenium
# from selenium.webdriver.common.by import By

from lk_megafon import run_lk_megafon
from lk_beeline import run_lk_beeline
from bid_beeline import run_bid_beeline
from bid_rostelecom2 import run_bid_rostelecom2
from bid_rostelecom import run_bid_rostelecom
from bid_mts import run_bid_mts
from bid_domru import run_bid_domru
from bid_ttk import run_bid_ttk
from bid_onlime import run_bid_onlime
from bid_mgts import run_bid_mgts

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
TIME_10_SECONDS = 10  # в секундах, 
TIME_3_SECONDS = 3  # в секундах, 
PERIOD_BETWEEN = 1  # в секундах, Пауза


if __name__ == '__main__':
    dtn = datetime.now()  # Стартовать с отсрочкой PERIOD_BETWEEN
    dtn = dtn - timedelta(hours=5)  # Стартовать сразу

    start_time_bid_beeline = dtn
    start_time_bid_mts = dtn
    start_time_bid_rostelecom2 = dtn
    start_time_bid_rostelecom = dtn
    start_time_bid_domru = dtn
    start_time_bid_ttk = dtn
    start_time_bid_onlime = dtn
    start_time_bid_mgts = dtn
    start_time_lk_megafon = dtn
    start_time_lk_beeline = dtn
    
    while True:
        time.sleep(PERIOD_BETWEEN)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        
        #===============================================#
        # Скрипт Заведение заявок beeline
        cur_time = datetime.now()
        if (cur_time - start_time_bid_beeline).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_beeline'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_beeline, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_beeline, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_beeline = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок mts
        cur_time = datetime.now()
        if (cur_time - start_time_bid_mts).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_mts'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_mts, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_mts, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_mts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок rostelecom2
        cur_time = datetime.now()
        if (cur_time - start_time_bid_rostelecom2).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_rostelecom2'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_rostelecom2, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_rostelecom2, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_rostelecom2 = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок rostelecom
        cur_time = datetime.now()
        if (cur_time - start_time_bid_rostelecom).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_rostelecom'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_rostelecom, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_rostelecom, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_rostelecom = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок domru
        cur_time = datetime.now()
        if (cur_time - start_time_bid_domru).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_domru'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_domru, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_domru, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_domru = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок ttk
        cur_time = datetime.now()
        if (cur_time - start_time_bid_ttk).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_ttk'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_ttk, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_ttk, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_ttk = cur_time
                time.sleep(0.2)

        # #===============================================#
        # # Скрипт Заведение заявок onlime
        # cur_time = datetime.now()
        # if (cur_time - start_time_bid_onlime).seconds >= TIME_3_SECONDS:
            # thread_name = 'bid_onlime'
            # is_run = False
            # for thread in threading.enumerate():
                # if thread.getName() == thread_name: is_run = True; break
            # if is_run == False:
                # # th = threading.Thread(target=run_bid_onlime, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                # th = threading.Thread(target=run_bid_onlime, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                # th.start()
                # print(f'Bot: {thread_name} is running.')
                # start_time_bid_onlime = cur_time
                # time.sleep(0.2)

        #===============================================#
        # Скрипт Заведение заявок mgts
        cur_time = datetime.now()
        if (cur_time - start_time_bid_mgts).seconds >= TIME_3_SECONDS:
            thread_name = 'bid_mgts'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_bid_mgts, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_bid_mgts, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_bid_mgts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт парсинг ЛК megafon
        cur_time = datetime.now()
        if (cur_time - start_time_lk_megafon).seconds >= TIME_1_HOUR:
            thread_name = 'lk_megafon'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_lk_megafon, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_lk_megafon, name=thread_name, args=(LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_lk_megafon = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт парсинг ЛК beeline
        cur_time = datetime.now()
        if (cur_time - start_time_lk_beeline).seconds >= TIME_1_HOUR:
            thread_name = 'lk_beeline'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_lk_beeline, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_lk_beeline, name=thread_name, args=(LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_lk_beeline = cur_time
                time.sleep(0.2)

    #####################################################
