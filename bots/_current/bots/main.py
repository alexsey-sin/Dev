import os
import time
from datetime import datetime
import logging

from lk_mts import run as run_lk_mts

logging.basicConfig(
    level=logging.DEBUG,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
    filename='log_main.log',
    datefmt='%d.%m.%Y %H:%M:%S',
    format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
)

# # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
# TELEGRAM_CHAT_ID = '1740645090'
# TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# # общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
# BID_TELEGRAM_CHAT_ID = '-1001646764735'
# BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

# Константы
PERIOD_10_SEC = 10
PERIOD_1_SEC = 1
PERIOD_1_HOUR = 60 * 60


if __name__ == '__main__':
    stm_lk_mts = None
    
    # log.debug("This is a debug message")
    # log.info("Informational message")
    # log.error("An error has happened!")
    
    while True:
        time.sleep(PERIOD_1_SEC)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        str_time = cur_time.strftime('%H:%M:%S %d.%m.%Y')
        
        #===============================================#
        # Скрипт Сбор_инфо ЛК МТС
        if stm_lk_mts:
            passed = (cur_time - stm_lk_mts).seconds
        if stm_lk_mts == None or passed >= PERIOD_1_HOUR:
            stm_lk_mts = cur_time
            logging.info('Старт "Сбор_инфо ЛК МТС"')
            run_lk_mts(logging)
            continue

        #===============================================#
        # # Скрипт Проверка ТхВ mts
        # if start_time_txv_mts:
            # passed = (cur_time - start_time_txv_mts).seconds
        # if start_time_txv_mts == None or passed >= PERIOD_SCAN_TXV_MTS:
            # start_time_txv_mts = cur_time
            # print(f'start txv_mts {str_time}')
            # run_txv_mts(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_mts(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        #===============================================#


        #===============================================#

    #####################################################
