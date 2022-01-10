import os
import time
from datetime import datetime

from txv_beeline import run_txv_beeline
from txv_mts import run_txv_mts
from txv_domru import run_txv_domru
from txv_rostelecom import run_txv_rostelecom
from txv_ttk import run_txv_ttk
from txv_onlime import run_txv_onlime
from txv_mgts import run_txv_mgts

# личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
BID_TELEGRAM_CHAT_ID = '-1001646764735'
BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

PERIOD_SCAN_TXV_BEELINE = 10  # Периодичность работы скрипта запроса тхв BEELINE
PERIOD_SCAN_TXV_MTS = 10  # Периодичность работы скрипта запроса тхв MTS
PERIOD_SCAN_TXV_DOMRU = 10  # Периодичность работы скрипта запроса тхв DOMRU
PERIOD_SCAN_TXV_ROSTELECOM = 10  # Периодичность работы скрипта запроса тхв ROSTELECOM
PERIOD_SCAN_TXV_TTK = 10  # Периодичность работы скрипта запроса тхв TTK
PERIOD_SCAN_TXV_ONLIME = 10  # Периодичность работы скрипта запроса тхв ONLIME
PERIOD_SCAN_TXV_MGTS = 10  # Периодичность работы скрипта запроса тхв MGTS
PERIOD_BETWEEN = 1  # в секундах, Пауза


if __name__ == '__main__':
    start_time_txv_beeline = None
    start_time_txv_mts = None
    start_time_txv_domru = None
    start_time_txv_rostelecom = None
    start_time_txv_ttk = None
    start_time_txv_onlime = None
    start_time_txv_mgts = None
    
    while True:
        time.sleep(PERIOD_BETWEEN)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        str_time = cur_time.strftime('%H:%M:%S %d-%m-%Y')
        
        #===============================================#
        # Скрипт Проверка ТхВ beeline
        if start_time_txv_beeline:
            passed = (cur_time - start_time_txv_beeline).seconds
        if start_time_txv_beeline == None or passed >= PERIOD_SCAN_TXV_BEELINE:
            start_time_txv_beeline = cur_time
            print(f'start txv_beeline {str_time}')
            run_txv_beeline(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_beeline(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#
        # Скрипт Проверка ТхВ mts
        if start_time_txv_mts:
            passed = (cur_time - start_time_txv_mts).seconds
        if start_time_txv_mts == None or passed >= PERIOD_SCAN_TXV_MTS:
            start_time_txv_mts = cur_time
            print(f'start txv_mts {str_time}')
            run_txv_mts(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_mts(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

        # Скрипт Проверка ТхВ domru
        if start_time_txv_domru:
            passed = (cur_time - start_time_txv_domru).seconds
        if start_time_txv_domru == None or passed >= PERIOD_SCAN_TXV_DOMRU:
            start_time_txv_domru = cur_time
            print(f'start txv_domru {str_time}')
            run_txv_domru(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_domru(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

        # Скрипт Проверка ТхВ rostelecom
        if start_time_txv_rostelecom:
            passed = (cur_time - start_time_txv_rostelecom).seconds
        if start_time_txv_rostelecom == None or passed >= PERIOD_SCAN_TXV_ROSTELECOM:
            start_time_txv_rostelecom = cur_time
            print(f'start txv_rostelecom {str_time}')
            run_txv_rostelecom(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_rostelecom(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

        # Скрипт Проверка ТхВ ttk
        if start_time_txv_ttk:
            passed = (cur_time - start_time_txv_ttk).seconds
        if start_time_txv_ttk == None or passed >= PERIOD_SCAN_TXV_TTK:
            start_time_txv_ttk = cur_time
            print(f'start txv_ttk {str_time}')
            run_txv_ttk(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_ttk(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

        # Скрипт Проверка ТхВ onlime
        if start_time_txv_onlime:
            passed = (cur_time - start_time_txv_onlime).seconds
        if start_time_txv_onlime == None or passed >= PERIOD_SCAN_TXV_ONLIME:
            start_time_txv_onlime = cur_time
            print(f'start txv_onlime {str_time}')
            run_txv_onlime(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # run_txv_onlime(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

        # Скрипт Проверка ТхВ mgts
        if start_time_txv_mgts:
            passed = (cur_time - start_time_txv_mgts).seconds
        if start_time_txv_mgts == None or passed >= PERIOD_SCAN_TXV_MGTS:
            start_time_txv_mgts = cur_time
            print(f'start txv_mgts {str_time}')
            # run_txv_mgts(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            run_txv_mgts(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            continue

        #===============================================#

    #####################################################
