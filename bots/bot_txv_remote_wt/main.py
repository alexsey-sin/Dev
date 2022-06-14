import os, time, threading, logging
from datetime import datetime, timedelta, time as dt_time

from txv_beeline import run_txv_beeline
from txv_mts import run_txv_mts
from txv_domru import run_txv_domru
from txv_rostelecom import run_txv_rostelecom
from txv_ttk import run_txv_ttk
from txv_onlime import run_txv_onlime
from txv_mgts import run_txv_mgts
from txv_multi_regions import run_txv_multi_regions
from pv_rostelecom import run_check_deals as run_pv_rostelecom
from pv_beeline import run_check_deals as run_pv_beeline
from pv_domru import run_check_deals as run_pv_domru
from pv_mts import run_check_deals as run_pv_mts
from pv_onlime import run_check_deals as run_pv_onlime

# личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot Автозаявки        BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN
BID_TELEGRAM_CHAT_ID = '-1001646764735'
BID_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

TIME_3_SECONDS = 3  # в секундах, 
PERIOD_BETWEEN = 0.5  # в секундах, Пауза

time_pv_rostelecom = {'h': 1, 'm': 0, 's': 0}
time_pv_beeline = {'h': 1, 'm': 10, 's': 0}
time_pv_domru = {'h': 1, 'm': 20, 's': 0}
time_pv_mts = {'h': 1, 'm': 30, 's': 0}
time_pv_onlime = {'h': 1, 'm': 40, 's': 0}

logging.basicConfig(
    level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
    filename='main_log.log',
    datefmt='%d.%m.%Y %H:%M:%S',
    format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
)
logging.getLogger('urllib3').setLevel(logging.CRITICAL)
logging.getLogger('undetected_chromedriver.patcher').setLevel(logging.CRITICAL)  # чтобы узнать кто постит в лог добавить в format :%(name)s:
logger = logging.getLogger(__name__)


def its_time(dct_time):
    pv_t = time.localtime()
    if pv_t.tm_hour == dct_time['h'] and pv_t.tm_min == dct_time['m'] and pv_t.tm_sec == dct_time['s']: return True
    else: return False


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
    
    thread_name_beeline = 'txv_beeline'
    thread_name_mts = 'txv_mts'
    thread_name_domru = 'txv_domru'
    thread_name_ttk = 'txv_ttk'
    thread_name_onlime = 'txv_onlime'
    thread_name_mgts = 'txv_mgts'
    thread_name_rostelecom = 'txv_rostelecom'
    thread_name_multi_regions = 'txv_multi_regions'
    
    thread_name_pv_rostelecom = 'pv_rostelecom'
    thread_name_pv_beeline = 'pv_beeline'
    thread_name_pv_domru = 'pv_domru'
    thread_name_pv_mts = 'pv_mts'
    thread_name_pv_onlime = 'pv_onlime'

    
    while True:
        time.sleep(PERIOD_BETWEEN)
        # Рабочее время ботов с 6 до 23
        cur_time = datetime.now()
        
        if cur_time.hour < 6 or cur_time.hour >= 23:
            # Ночное время - работают боты ПВ
            if its_time(time_pv_rostelecom):
                is_run = False
                for thread in threading.enumerate():
                    if thread.getName() == thread_name_pv_rostelecom: is_run = True; break
                if is_run == False:
                    logger.info(f'Start {thread_name_pv_rostelecom} thread')
                    # th = threading.Thread(target=run_pv_rostelecom, name=thread_name_pv_rostelecom, args=(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                    th = threading.Thread(target=run_pv_rostelecom, name=thread_name_pv_rostelecom, args=(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN))
                    th.start()
                time.sleep(1)
            
            if its_time(time_pv_beeline):
                is_run = False
                for thread in threading.enumerate():
                    if thread.getName() == thread_name_pv_beeline: is_run = True; break
                if is_run == False:
                    logger.info(f'Start {thread_name_pv_beeline} thread')
                    # th = threading.Thread(target=run_pv_beeline, name=thread_name_pv_beeline, args=(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                    th = threading.Thread(target=run_pv_beeline, name=thread_name_pv_beeline, args=(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN))
                    th.start()
                time.sleep(1)
            
            if its_time(time_pv_domru):
                is_run = False
                for thread in threading.enumerate():
                    if thread.getName() == thread_name_pv_domru: is_run = True; break
                if is_run == False:
                    logger.info(f'Start {thread_name_pv_domru} thread')
                    # th = threading.Thread(target=run_pv_domru, name=thread_name_pv_domru, args=(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                    th = threading.Thread(target=run_pv_domru, name=thread_name_pv_domru, args=(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN))
                    th.start()
                time.sleep(1)
            
            if its_time(time_pv_mts):
                is_run = False
                for thread in threading.enumerate():
                    if thread.getName() == thread_name_pv_mts: is_run = True; break
                if is_run == False:
                    logger.info(f'Start {thread_name_pv_mts} thread')
                    # th = threading.Thread(target=run_pv_mts, name=thread_name_pv_mts, args=(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                    th = threading.Thread(target=run_pv_mts, name=thread_name_pv_mts, args=(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN))
                    th.start()
                    print(f'Bot: {thread_name_pv_mts} is running.')
                time.sleep(1)
            
            if its_time(time_pv_onlime):
                is_run = False
                for thread in threading.enumerate():
                    if thread.getName() == thread_name_pv_onlime: is_run = True; break
                if is_run == False:
                    logger.info(f'Start {thread_name_pv_onlime} thread')
                    # th = threading.Thread(target=run_pv_mts, name=thread_name_pv_onlime, args=(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                    th = threading.Thread(target=run_pv_mts, name=thread_name_pv_onlime, args=(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN))
                    th.start()
                    print(f'Bot: {thread_name_pv_onlime} is running.')
                time.sleep(1)
            
            continue
        
        #===============================================#
        # Скрипт Проверка ТхВ beeline
        cur_time = datetime.now()
        if (cur_time - start_time_txv_beeline).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_beeline: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_beeline, name=thread_name_beeline, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_beeline, name=thread_name_beeline, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_beeline} is running.')
                start_time_txv_beeline = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ mts
        cur_time = datetime.now()
        if (cur_time - start_time_txv_mts).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_mts: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_mts, name=thread_name_mts, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_mts, name=thread_name_mts, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_mts} is running.')
                start_time_txv_mts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ domru
        cur_time = datetime.now()
        if (cur_time - start_time_txv_domru).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_domru: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_domru, name=thread_name_domru, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_domru, name=thread_name_domru, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_domru} is running.')
                start_time_txv_domru = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ ttk
        cur_time = datetime.now()
        if (cur_time - start_time_txv_ttk).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_ttk: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_ttk, name=thread_name_ttk, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_ttk, name=thread_name_ttk, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_ttk} is running.')
                start_time_txv_ttk = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ onlime
        cur_time = datetime.now()
        if (cur_time - start_time_txv_onlime).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_onlime: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_onlime, name=thread_name_onlime, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_onlime, name=thread_name_onlime, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_onlime} is running.')
                start_time_txv_onlime = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ mgts
        cur_time = datetime.now()
        if (cur_time - start_time_txv_mgts).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_mgts: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_mgts, name=thread_name_mgts, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_mgts, name=thread_name_mgts, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_mgts} is running.')
                start_time_txv_mgts = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ rostelecom
        cur_time = datetime.now()
        if (cur_time - start_time_txv_rostelecom).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_rostelecom: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_rostelecom, name=thread_name_rostelecom, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_rostelecom, name=thread_name_rostelecom, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_rostelecom} is running.')
                start_time_txv_rostelecom = cur_time
                time.sleep(0.2)

        #===============================================#
        # Скрипт Проверка ТхВ multi_regions
        cur_time = datetime.now()
        if (cur_time - start_time_multi_regions).seconds >= TIME_3_SECONDS:
            is_run = False
            for thread in threading.enumerate():
                if thread.getName() == thread_name_multi_regions: is_run = True; break
            if is_run == False:
                # th = threading.Thread(target=run_txv_rostelecom, name=thread_name_multi_regions, args=(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN))
                th = threading.Thread(target=run_txv_multi_regions, name=thread_name_multi_regions, args=(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN))
                th.start()
                print(f'Bot: {thread_name_multi_regions} is running.')
                start_time_multi_regions = cur_time
                time.sleep(0.2)

        #===============================================#

    #####################################################
