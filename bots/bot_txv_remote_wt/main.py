import os, time, threading
from datetime import datetime, timedelta

from txv_beeline import run_txv_beeline
from txv_mts import run_txv_mts
from txv_domru import run_txv_domru
from txv_rostelecom import run_txv_rostelecom
from txv_ttk import run_txv_ttk
from txv_onlime import run_txv_onlime
from txv_mgts import run_txv_mgts
from txv_multi_regions import run_txv_multi_regions

# личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
BID_TELEGRAM_CHAT_ID = '-1001646764735'
BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

TIME_3_SECONDS = 3  # в секундах, 
PERIOD_BETWEEN = 1  # в секундах, Пауза


if __name__ == '__main__':
    dtn = datetime.now()  # Стартовать с отсрочкой PERIOD_BETWEEN
    dtn = dtn - timedelta(hours=5)  # Стартовать сразу
    
    start_time_txv_beeline = dtn
    start_time_txv_mts = dtn
    start_time_txv_domru = dtn
    start_time_txv_rostelecom = dtn
    start_time_txv_ttk = dtn
    start_time_txv_onlime = dtn
    start_time_txv_mgts = dtn
    start_time_multi_regions = dtn
    
    while True:
        time.sleep(PERIOD_BETWEEN)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        
        #===============================================#
        # Скрипт Проверка ТхВ beeline
        cur_time = datetime.now()
        if (cur_time - start_time_txv_beeline).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_beeline'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_beeline, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_beeline, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_beeline = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ mts
        cur_time = datetime.now()
        if (cur_time - start_time_txv_mts).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_mts'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_mts, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_mts, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_mts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ domru
        cur_time = datetime.now()
        if (cur_time - start_time_txv_domru).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_domru'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_domru, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_domru, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_domru = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ ttk
        cur_time = datetime.now()
        if (cur_time - start_time_txv_ttk).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_ttk'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_ttk, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_ttk, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_ttk = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ onlime
        cur_time = datetime.now()
        if (cur_time - start_time_txv_onlime).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_onlime'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_onlime, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_onlime, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_onlime = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ mgts
        cur_time = datetime.now()
        if (cur_time - start_time_txv_mgts).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_mgts'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                th = threading.Thread(target=run_txv_mgts, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                # th = threading.Thread(target=run_txv_mgts, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_mgts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ rostelecom
        cur_time = datetime.now()
        if (cur_time - start_time_txv_rostelecom).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_rostelecom'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_rostelecom, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_rostelecom, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_txv_rostelecom = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ multi_regions
        cur_time = datetime.now()
        if (cur_time - start_time_multi_regions).seconds >= TIME_3_SECONDS:
            thread_name = 'txv_multi_regions'
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_rostelecom, name=thread_name, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_multi_regions, name=thread_name, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name} is running.')
                start_time_multi_regions = cur_time
                time.sleep(0.2)

        #===============================================#

    #####################################################
