import os, time, re, json, logging
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000'
url_host = 'http://django.domconnect.ru'
provider = 'Билайн'
pv_crm_code = 'OTHER'  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 1  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

acc_data = {  # Доступы к ПВ
    'url': 'https://partnerweb.beeline.ru/',
    'partners': [
        {
            'code': '3002',     # (СПб и ЛО, БМ)
            'login': '0K23-181',
            'employee': '1010000101',
            'password': 'FudlU7tfFsK5g6',
            'deals': [],
        },
        {
            'code': '3058',     # (МО и МСК)
            'login': 'S01-181',
            'employee': '1999999222',
            'password': '8GFysus@kffs7',
            'deals': [],
        },
        {
            'code': '3003',     # (РФ)
            'login': 'S24-61',
            'employee': '1010000101',
            'password': 'Ft&dhdk234hbs3',
            'deals': [],
        },
    ]
}
status_beeline_srm = {  # Коды статусов: Билайн = СРМ
    'Подключен': 2,  # Подключен
    'Отказ': 'NEW',  # Ошибки + коммент
    'Принято в обзвон': 'NEW',  # Ошибки + коммент
    'Позвонить клиенту': 'NEW',  # Ошибки + коммент
    'Ждем звонка клиента': 'NEW',  # Ошибки + коммент
    'Мусор': 'NEW',  # Ошибки + коммент
    'Резерв': 'NEW',  # Ошибки + коммент
    'Отложенная продажа': 'NEW',  # Ошибки + коммент
}
name_status_crm = {
    2: 'Подключен',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы Билайн когда требуется взять коментарий из истории
    'Отказ',
    'Принято в обзвон',
    'Закрыта',
    'Позвонить клиенту',
    'Ждем звонка клиента',
    'Мусор',
    'Резерв',
    'Отложенная продажа',
]


def get_deals_crm(pv, from_data, to_date, pw_code):
    url = 'https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.list'
    
    go_next = 0
    go_total = 0
    out_lst = []

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    while True:
        data = {
            'start': go_next,
            'order': {'ID': 'ASC'},  # Если нужно с сортировкой
            'filter': {
                '>=DATE_CREATE': from_data,  # '2021-10-01T00:00:00'
                '<DATE_CREATE': to_date,  # '2021-10-01T00:00:00'
                'UF_CRM_5903C16B84C55': pv,  # Провайдер
                'STAGE_ID': [1, 5],
                'UF_CRM_595ED493B6E5C': pw_code,  # PartnerWEB
                'UF_CRM_595E343AA0EE2': 0,  # Юр. лицо
            },
            'select': [
                'ID',
                'DATE_CREATE',
                'STAGE_ID',
                'UF_CRM_5903C16BDF7A7',  # Номер заявки
                'UF_CRM_595ED493B6E5C',  # PartnerWEB
            ]
        }
        try:
            responce = requests.post(url, headers=headers, json=data)
            if responce.status_code == 200:
                answer = json.loads(responce.text)
                result = answer.get('result')
                # print(result)
                go_next = answer.get('next')
                go_total = answer.get('total')
                out_lst += result
                print(go_next, go_total)
                if not go_next: break
            else:
                return f'Ошибка get_deals: responce.status_code: {responce.status_code}\n{responce.text}', []
        except:
            return 'Ошибка get_deals: try: requests.post', []
        time.sleep(1)
    return '', out_lst
    # https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.list?
    # order[id]=DESC&filter[>DATE_CREATE]=2022-03-01&filter[UF_CRM_5903C16B84C55]=3&filter[STAGE_ID]=1&filter[UF_CRM_595E343AA0EE2]=0&select[]=UF_CRM_5903C16BDF7A7&select[]=STAGE_ID&select[]=DATE_CREATE&select[]=UF_CRM_595ED493B6E5C
    pass

def wait_spinner(driver):  # Ожидаем крутящийся спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-spinner")]')
        if len(els):
            # print('ju-spinner')
            pass
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

# =========================================================
def get_deal_status(logger, acc_data):
    driver = None
    try:
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        
        for a_data in acc_data['partners']:
            driver = webdriver.Chrome(service=service)
            driver.implicitly_wait(10)
            driver.get(acc_data.get('url'))
            time.sleep(3)
            
            # ###################### Login ######################
            els = driver.find_elements(By.ID, 'id_login')
            if len(els) != 1: raise Exception('Ошибка нет поля логин')
            login = a_data.get('login')
            try: 
                if login: els[0].send_keys(login)
                else: raise Exception('Ошибка не задан логин')
            except: raise Exception('Ошибка действий 01')
            time.sleep(1)
            
            workercode = a_data.get('employee')
            if not workercode: raise Exception('Ошибка не задан PartnerWeb (employee)')
            els = driver.find_elements(By.ID, 'id_workercode')
            if len(els) != 1: raise Exception('Ошибка нет поля workercode')
            try: els[0].send_keys(workercode)
            except: raise Exception('Ошибка действий 02')
            time.sleep(1)

            els = driver.find_elements(By.ID, 'id_password')
            if len(els) != 1: raise Exception('Ошибка нет поля пароль')
            password = a_data.get('password')
            try:
                if password: els[0].send_keys(password)
                else: raise Exception('Ошибка не задан пароль')
            except: raise Exception('Ошибка действий 03')
            time.sleep(1)

            els = driver.find_elements(By.TAG_NAME, 'button')
            if len(els) != 1: raise Exception('Ошибка нет кнопки войти')
            try: els[0].click()
            except: raise Exception('Ошибка действий 04')
            time.sleep(5)
            ###################### Главная страница ######################
            # проход по всем заявкам
            for deal in a_data['deals']:
                num = deal.get('num')
                if not num or deal.get('pv_status') == 'deal_number_error':
                    log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}'
                    logger.info(log_mess)
                    continue
                els = driver.find_elements(By.XPATH, '//input[@placeholder="Введите номер"]')
                if len(els) != 1: raise Exception('Нет поля ввода номера заявки')
                els_btn = driver.find_elements(By.XPATH, '//button[contains(@ng-click, "applyFilterHander")]')
                if len(els_btn) != 1: raise Exception('Нет кнопки применить фильтр')
                # вводим номер заявки
                try:
                    els[0].send_keys(Keys.CONTROL + 'a')
                    time.sleep(1)
                    els[0].send_keys(Keys.DELETE)
                    time.sleep(1)
                    els[0].send_keys(num)
                    time.sleep(1)
                    els_btn[0].click()
                    time.sleep(1)
                except: raise Exception('Ошибка ввода номера заявки')
                time.sleep(2)
                
                # Посмотрим строку результата
                driver.implicitly_wait(1)
                els = driver.find_elements(By.XPATH, '//tr[contains(@class, "tr--hovered")]')
                driver.implicitly_wait(10)
                if len(els) > 0:
                    els_td = els[0].find_elements(By.TAG_NAME, 'td')
                    if len(els_td) != 9: raise Exception('Неправильный формат строки таблицы результатов поиска заявки')
                    status = els_td[3].text
                    # print(status)
                    deal['pv_status'] = status
                    # Анализируем статус
                    for stat_b in status_beeline_srm.keys():
                        if status.find(stat_b) >= 0:
                            if deal['pv_status'] == 'Подключен':
                                deal['date_connect'] = status[len(stat_b):].strip()
                            break

                    
                    cast_status = deal.get('pv_status')
                    if cast_status in status_for_comment:
                        time.sleep(2)
                        # Требуется взять комментарий
                        # По нормальному тэг svg selenium не находит
                        els_svg = driver.find_elements(By.XPATH, '//*[local-name() = "svg" and (@ng-click="ticket.expandedTicket()")]')
                        try: els_svg[0].click()
                        except: raise Exception('Ошибка раскрытия коментария')

                        els_comm = driver.find_elements(By.XPATH, '//div[@ng-bind-html="comment.text"]')
                        if len(els_comm) > 0: deal['comment'] = els_comm[0].text
                    
                else:
                    deal['pv_status'] = 'not_found'
                    deal['comment'] = 'Заявка в ЛК не найдена'

                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("date_connect", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
            # with open('out.html', 'w', encoding='utf-8') as outfile:
                # outfile.write(driver.page_source)
            # raise Exception('Финиш.')
            
            driver.quit()
            driver = None
            time.sleep(2)


    

    except Exception as e:
        return str(e)[:100], acc_data
    finally:
        if driver: driver.quit()
   
    return '', acc_data

def send_crm_deal_stage(deal, new_code_stage):
    url = 'https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.update'
    # HELP: https://dev.1c-bitrix.ru/rest_help/crm/cdeals/crm_deal_update.php

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    
    # Собираем данные
    data = {
        'id': deal.get('ID'),
        'fields': 
            {
                'STAGE_ID': new_code_stage,
            }
    }
    comment = deal.get('comment')
    if comment: data['fields']['UF_CRM_59B40B8474D0A'] = comment
    if new_code_stage == 2: data['fields']['UF_CRM_5904FB99DBF0C'] = deal.get('date_connect', '')
    
    # Отсылаем
    try:
        responce = requests.post(url, headers=headers, json=data)
        st_code = responce.status_code
        if st_code != 200: return st_code
    except Exception as e:
        return str(e)
        
    return ''
    
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

def get_dc_token():
    url = url_host + '/auth/jwt/create/'
    
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'username': 'user',
        'password': 'User123456'
    }
    
    try:
        responce = requests.post(url, headers=headers, json=data)
        answer = json.loads(responce.text)
        return answer.get('access', '')
    except: return ''

def send_dj_domconnect_result(lst_deal):
    dc_token = get_dc_token()
    if not dc_token: return 'not_token'
    
    url = url_host + '/api/set_pv_result/'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {dc_token}',
    }
    data = []
    for deal in lst_deal:
        dct = {
            'pv_code': pv_dc_code,
            'id_crm': deal.get('ID', 'Не определен')[:50],
            'num_deal': deal.get('num', 'Не определен')[:50],
            'pv_status': deal.get('pv_status', '')[:255],
            'crm_status': deal.get('crm_status', ''),
            'date_connect': deal.get('date_connect', '')[:50],
            'comment': deal.get('comment', ''),
        }
        data.append(dct)
    
    try:
        responce = requests.post(url, headers=headers, json=data)
        if responce.status_code != 200:
            return str(responce.text)[:100]
    except Exception as e: return str(e)[:100]

    return ''

def run_check_deals(logger, tlg_chat, tlg_token, by_days=60):
    logger.info(f'Старт ПВ: {provider}')

    # Определим диапазон дат для фильтра
    cur_date = datetime.today()
    to_date = cur_date.date()
    from_date = (cur_date - timedelta(days=by_days)).date()
    
    # Соберем список кодов по PartnerWEB
    pw_code = [x['code'] for x in acc_data['partners']]
    
    # Заберем сделки из СРМ по фильтру
    e, lst_deal = get_deals_crm(pv_crm_code, str(from_date), str(to_date), pw_code)
    if e: 
        log_mess = f'ПВ {provider}: загрузка сделок из срм: {e}'
        logger.error(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return
    if len(lst_deal) == 0:
        log_mess = f'ПВ {provider}: Сделок нет'
        logger.info(log_mess); print(log_mess)
        return

    log_mess = f'ПВ {provider}: Исходный список: {len(lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    
    # Соберем нормальный список сделок
    new_lst_deal = []
    for dl in lst_deal:
        num = dl.get('UF_CRM_5903C16BDF7A7').strip()
        id_d = dl.get('ID')
        num_out = ''
        pw_code = dl.get('UF_CRM_595ED493B6E5C').strip()
        dct = {'ID': id_d, 'num': num, 'pw_code': pw_code}
        if not num.isdigit():  # Просто один номер
            error = False
            num_e = num.replace('/', ' ')
            num_e = num.replace('№', '')
            lst_num = num_e.split(' ')
            l_num = [int(n.strip()) for n in lst_num if n.strip().isdigit()]
            if len(l_num) == 0:
                error = True
            elif len(l_num) == 1: dct['num'] = str(l_num[0])
            else:
                l_num.sort()
                error = True
                for i in range(1, len(l_num)):
                    if (l_num[i-1] + 1) == l_num[i]:
                        dct['num'] = str(l_num[i-1])
                        error = False
            if error:
                dct['pv_status'] = 'deal_number_error'
                dct['comment'] = 'Ошибка номера сделки'
        new_lst_deal.append(dct)
    log_mess = f'ПВ {provider}: Нормализованный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    
    # Составим списки сделок по PartnerWEB
    for deal in new_lst_deal:
        is_ok = False
        for a_data in acc_data['partners']:
            if deal.get('pw_code', '') == a_data.get('code'):
                is_ok = True
                a_data['deals'].append(deal)
        if is_ok == False:
            print('pw_code is not:', deal.get('pw_code'))
    
    # Проверим статус сделок у ПВ
    e, new_acc_data = get_deal_status(logger, acc_data)
    if e: 
        log_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return
    
    # Проверим статус на подлежащие изменению в СРМ
    change = 0
    cnt_all = 0
    for partner in new_acc_data['partners']:
        cnt_all += len(partner['deals'])
        for deal in partner['deals']:
            status = deal.get('pv_status')
            if status and status in status_beeline_srm:
                deal['crm_status'] = status_beeline_srm[status]
                # print(deal.get('ID'), status, name_status_crm[status_beeline_srm[status]])
                e = send_crm_deal_stage(deal, status_beeline_srm[status])
                # e = False
                if e: 
                    log_mess = f'ПВ {provider}: Ошибка при обновлении статуса сделки в срм: {e}'
                    logger.info(log_mess); print(log_mess)
                    send_telegram(tlg_chat, tlg_token, log_mess)
                else: change += 1
                time.sleep(0.5)
        e = send_dj_domconnect_result(partner['deals'])
        if e:
            log_mess = f'ПВ {provider}: Ошибка при архивировании сделки в dj_domconnect: {e}'
            logger.info(log_mess); print(log_mess)
            send_telegram(tlg_chat, tlg_token, log_mess)

    tlg_mess = f'ПВ {provider}:\nСтатус сделок изменен\nв {change} из {len(lst_deal)}\n'
    str_today = datetime.today().strftime('%d.%m.%Y')
    tlg_mess += f'http://django.domconnect.ru/api/get_pv_result/{pv_dc_code}/{str_today}'
    if e: tlg_mess += f'\nОшибка архивации: {e}'
    
    e = send_telegram(tlg_chat, tlg_token, tlg_mess)
    logger.info(tlg_mess.replace('\n', ''))
    logger.info(f'Финиш ПВ: {provider} {e}')


if __name__ == '__main__':
    os.system('cls')
    logging.basicConfig(
        level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
        filename='main_log.log',
        datefmt='%d.%m.%Y %H:%M:%S',
        format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
    )
    logging.getLogger('urllib3').setLevel(logging.CRITICAL)
    logging.getLogger('undetected_chromedriver.patcher').setLevel(logging.CRITICAL)  # чтобы узнать кто постит в лог добавить в format :%(name)s:
    logger = logging.getLogger(__name__)
    
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN)
    # acc_data = {  # Доступы к ПВ
        # 'url': 'https://partnerweb.beeline.ru/',
        # 'partners': [
            # {
                # 'code': '3002',     # (СПб и ЛО, БМ)
                # 'login': '0K23-181',
                # 'employee': '1010000101',
                # 'password': 'FudlU7tfFsK5g6',
                # 'deals': [
                    # {
                        # "ID": "158869",
                        # "num": "244091891",
                        # "pw_code": "3002",
                    # },
                    # {
                        # "ID": "158582",
                        # "num": "243608801",
                        # "pw_code": "3002",
                    # },
                # ],
            # },
            # # {
                # # 'code': '3058',     # (МО и МСК)
                # # 'login': 'S01-181',
                # # 'employee': '1999999222',
                # # 'password': '8GFysus@kffs7',
                # # 'deals': [],
            # # },
            # # {
                # # 'code': '3003',     # (РФ)
                # # 'login': 'S24-61',
                # # 'employee': '1010000101',
                # # 'password': 'Ft&dhdk234hbs3',
                # # 'deals': [
                    # # {
                        # # "ID": "156853",
                        # # "num": "243756326",
                        # # "pw_code": "3003",
                    # # }
                # # ],
            # # },
        # ]
    # }

    pass
    # e, acc_data = get_deal_status(acc_data)
    # if e: print(e)
    # print(acc_data)



