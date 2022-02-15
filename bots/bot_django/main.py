import os
import time
from datetime import datetime
import logging

# from lk_mts import run as run_lk_mts
from ats_trunk import run_ats

logging.basicConfig(
    level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
    filename='log_main.log',
    datefmt='%d.%m.%Y %H:%M:%S',
    format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
)
logger = logging.getLogger(__name__)

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
    stm_ats_trunk = None
    
    while True:
        time.sleep(PERIOD_1_SEC)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        if cur_time.hour < 6 or cur_time.hour >= 23: continue
        str_time = cur_time.strftime('%H:%M:%S %d.%m.%Y')
        
        #===============================================#
        # Скрипт АТС коррекция приоритетов транков
        if stm_ats_trunk:
            passed = (cur_time - stm_ats_trunk).seconds
        if stm_ats_trunk == None or passed >= PERIOD_1_HOUR:
            stm_ats_trunk = cur_time
            logger.info('Старт "АТС корр. транков"')
            run_ats(logger)
            continue

        # #===============================================#
        # # Скрипт Сбор_инфо ЛК МТС
        # if stm_lk_mts:
            # passed = (cur_time - stm_lk_mts).seconds
        # if stm_lk_mts == None or passed >= PERIOD_1_HOUR:
            # stm_lk_mts = cur_time
            # logger.info('Старт "Сбор_инфо ЛК МТС"')
            # run_lk_mts(logger)
            # continue


        #===============================================#


        #===============================================#

    #####################################################
'''
    Демон находится /etc/systemd/system/bots.service
    
    [Unit]
    Description=ATS domconnect bot
    After=network.target
    [Service]
    User=root
    Group=root
    WorkingDirectory=/var/www/bot_ats/
    EnvironmentFile=/etc/environment
    ExecStart=/var/www/bots/venv/bin/python3 main.py
    ExecReload=/var/www/bots/venv/bin/python3 main.py
    StandardOutput=syslog
    StandardError=syslog
    Restart=always
    RestartSec=15
    [Install]
    WantedBy=multi-user.target



'''