import os, time, re, json, logging
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000'
url_host = 'http://django.domconnect.ru'
provider = 'РТК'
pv_crm_code = 3  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 4  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

access = {  # Доступы к ПВ
    'url': 'https://eissd.rt.ru/login',
    'login': 'sz_v_an',
    'password': 'LzJ*%D6dQ{'
}
status_rtk_srm = {  # Коды статусов: РТК = СРМ
    'Услуга подключена': 2,  # Подключен
    'Отказ': 'NEW',  # Ошибки + коммент
    'Дубликат': 'NEW',  # Ошибки + коммент
    'Неверная заявка': 'NEW',  # Ошибки + коммент
    'Заявка не найдена': 'NEW',  # Ошибки + коммент
    'Тест': 11,  # Служебный
    'Продажа оборудования': 2,  # Подключен
    'Самоинсталляция / Доставка оборудования курьером, 0/1': 2,  # Подключен
}
prioritet_status = [
    'Домашний интернет',
    'Интерактивное ТВ',
    'Wink-ТВ-онлайн',
    'Мобильная связь',
]
name_status_crm = {
    2: 'Подключен',
    11: 'Служебный',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы РТК когда требуется взять коментарий из истории
    'Отказ',
    'Дубликат',
    'Неверная заявка',
]


def get_deals_crm(pv, from_data, to_date):
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
                'UF_CRM_595E343AA0EE2': 0,  # Юр. лицо
            },
            'select': [
                'ID',
                'DATE_CREATE',
                'STAGE_ID',
                'UF_CRM_5903C16BDF7A7',  # Номер заявки
                'UF_CRM_595ED493B6E5C',  # PartnerWEB
                'UF_CRM_5903C16BB2F06',  # Область
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
                if not go_next: break
                print(go_next, go_total)
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
def get_deal_status(logger, lst_deal, access, status_for_comment):
    driver = None
    try:
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(access.get('url'))
        time.sleep(3)
        
        # ###################### Login ######################
        login = access.get('login')
        if login:
            els = driver.find_elements(By.XPATH, '//input[@data-field="login"]')
            try: els[0].send_keys(login)
            except: raise Exception('Ошибка ввода логин')
            time.sleep(1)
        else: raise Exception('Ошибка не задан логин')

        password = access.get('password')
        if password:
            els = driver.find_elements(By.XPATH, '//input[@data-field="passw"]')
            try: els[0].send_keys(password)
            except: raise Exception('Ошибка ввода пароля')
            time.sleep(2)
        else: raise Exception('Ошибка не задан пароль')

        els = driver.find_elements(By.XPATH, '//input[@data-field="closeOthers"]')
        # Обычным способом чекбокс не отмечается - element not interactable
        try: driver.execute_script("arguments[0].click();", els[0])
        except: raise Exception('Ошибка отметки чекбокса закрыть другие сессии')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@value="Войти"]')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки авторизации')
        time.sleep(1)
        
        wait_spinner(driver)  # Подождем если есть спинер
        
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//div[@class="form-group error"]')
        if els: raise Exception(f'Ошибка {els[0].text}')  # Неверное имя пользователя или пароль
        driver.implicitly_wait(10)
        ###################### Главная страница ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/order/phys/list"]')
        if len(els) < 2: raise Exception('Нет ссылки Расширенный поиск заявок ФЛ')
        try: els[1].click()
        except: raise Exception('Ошибка клика ссылки перехода на страницу поиска заявки')
        time.sleep(3)
        ###################### Страница поиска заявки ######################
        # проверим всплывашки с рекламой
        driver.implicitly_wait(2)
        els = driver.find_elements(By.XPATH, '//div[@class="ju-popup ju-message user-messages-popup "]')
        for el in els:
            els_btn = el.find_elements(By.TAG_NAME, 'input')
            try: driver.execute_script("arguments[0].click();", els_btn[0])
            except: raise Exception('Ошибка закрытия окна всплывашки с рекламой')
            time.sleep(1)
        driver.implicitly_wait(10)

        # проход по всем заявкам
        for deal in lst_deal:
            deal['pv_status'] = ''
            num = deal.get('num')
            if not num:
                deal['num'] = 'Не определен'
                deal['pv_status'] = 'deal_number_error'
                continue
            if type(num) != str: num = str(num)
            # Проверим номер на правильность
            # Только цифры и длина от 8 до 13
            is_err_num = False
            num = num.strip()
            if not num.isdigit(): is_err_num = True
            l_num = len(num)
            if l_num < 8 or l_num > 13: is_err_num = True
            if is_err_num:
                deal['pv_status'] = 'deal_number_error'
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue
            
            els = driver.find_elements(By.XPATH, '//input[@name="packetNum"]')
            if len(els) != 1: raise Exception('Нет поля ввода номера заявки')
            # вводим номер заявки
            try:
                els[0].send_keys(Keys.CONTROL + 'a')
                time.sleep(1)
                els[0].send_keys(Keys.DELETE)
                time.sleep(1)
                els[0].send_keys(num)
            except: raise Exception('Ошибка ввода номера заявки')
            time.sleep(1)
            els = driver.find_elements(By.XPATH, '//input[contains(@class, "def-tabs-apply")]')
            if len(els) == 0: raise Exception('Нет кнопки поиска заявки')
            try: els[0].click()
            except:
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = 'Ошибка клика кнопки поиска заявки'
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue
            wait_spinner(driver)  # Подождем если есть спинер
            time.sleep(1)
            # Проверим нет ли всплывающего окна с сообщением Внимание
            driver.implicitly_wait(2)
            els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-popup ju-message attention")]')
            if len(els) == 1:
                els_cont = els[0].find_elements(By.XPATH, './/div[@class="content"]')
                if len(els_cont) > 0:
                    deal['pv_status'] = 'Заявка не найдена'
                    deal['comment'] = els_cont[0].text
                els_btn = els[0].find_elements(By.XPATH, './/input[contains(@class, "close")]')
                if len(els_btn) > 0:
                    try: els_btn[0].click()
                    except: raise Exception('Ошибка клика закрыть сообщение')
                time.sleep(2)
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue
            # Проверим нет ли всплывающего окна с сообщением Ошибка
            els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-popup ju-message error")]')
            if len(els) == 1:
                els_cont = els[0].find_elements(By.XPATH, './/div[@class="content"]')
                if len(els_cont) > 0:
                    deal['pv_status'] = 'deal_number_error'
                els_btn = els[0].find_elements(By.XPATH, './/input[contains(@class, "close")]')
                if len(els_btn) > 0:
                    try: els_btn[0].click()
                    except: raise Exception('Ошибка клика закрыть сообщение2')
                time.sleep(2)
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue

            driver.implicitly_wait(10)
            # Посмотрим результат
            els_div = driver.find_elements(By.XPATH, '//div[@id="filter_result"]')
            if len(els_div) == 0: raise Exception('Нет блока результатов поиска заявки')
            els_tbody = els_div[0].find_elements(By.TAG_NAME, 'tbody')
            if len(els_tbody) == 0:
                deal['pv_status'] = 'Заявка не найдена'
                deal['comment'] = 'Нет таблицы результатов поиска заявки'
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue
            els_tr = els_tbody[0].find_elements(By.TAG_NAME, 'tr')
            if len(els_tr) == 0: raise Exception('Нет строк таблицы результатов поиска заявки')
            
            print(num)
            status = ''
            date_connect = ''  # Дата подключения
            varied_status = False  # Разные статусы
            usluga_status = []  # список словарей: Услуга, статус, дата подключения
            for el_tr in els_tr:
                els_td = el_tr.find_elements(By.TAG_NAME, 'td')
                if len(els_td) != 14: raise Exception('Неправильный формат строки таблицы результатов поиска заявки')
                # Собираем статусы по строкам
                usluga_status.append({'usl': els_td[2].text, 'stat': els_td[7].text, 'data': els_td[8].text})
                if status == '':
                    status = els_td[7].text
                    date_connect = els_td[8].text
                    continue
                else:
                    if status != els_td[7].text: varied_status = True # Разные статусы по строкам

            if varied_status:
                # Проверим нет ли подключенных услуг
                not_ok = True
                for us_stat in usluga_status:
                    if us_stat.get('stat') == 'Услуга подключена':
                        deal['pv_status'] = us_stat.get('stat')
                        deal['date_connect'] = us_stat.get('data')
                        not_ok = False
                        break
                if not_ok:
                    f_ok = False
                    # Проход по приоритету статуса
                    for pr_st in prioritet_status:
                        for us_stat in usluga_status:
                            if us_stat.get('usl') == pr_st:
                                deal['pv_status'] = us_stat.get('stat')
                                deal['date_connect'] = us_stat.get('data')
                                f_ok = True
                                break
                        if f_ok: break
            else:
                if status: deal['pv_status'] = status
                if date_connect: deal['date_connect'] = date_connect
            try:
                if status in status_for_comment:
                    els_td = els_tr[0].find_elements(By.TAG_NAME, 'td')
                    els_a = els_td[13].find_elements(By.TAG_NAME, 'a')
                    els_a[0].click()
                    wait_spinner(driver)  # Подождем если есть спинер
                    time.sleep(1)
                    els_div_his = driver.find_elements(By.XPATH, '//div[contains(@class, "status-history-dialog")]')
                    els_tr = els_div_his[0].find_elements(By.TAG_NAME, 'tr')
                    els_td = els_tr[-1].find_elements(By.TAG_NAME, 'td')
                    comment = els_td[6].text
                    if comment.isdigit(): deal['comment'] = status
                    else: deal['comment'] = comment
                    # Закрываем
                    els_btn = els_div_his[0].find_elements(By.XPATH, './/input[contains(@class, "close")]')
                    if len(els_btn) > 0: els_btn[0].click()
                    time.sleep(1)
            except Exception as e: print(e)
            log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("date_connect", "")}|{deal.get("comment", "")}'
            logger.info(log_mess)
        
        
        #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        #===========

    

    except Exception as e:
        return str(e)[:100], lst_deal
    finally:
        if driver: driver.quit()
   
    return '', lst_deal

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

def send_dj_domconnect_result(logger, lst_deal):
    dc_token = get_dc_token()
    if not dc_token: return 'not_token'
    
    url = url_host + '/api/set_pv_result/'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {dc_token}',
    }
    data = []
    for deal in lst_deal:
        try:
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
        except Exception as e:
            log_mess = f'ПВ {provider}: Ошибка сбора списка сделок: {e}\n'
            log_mess += json.dumps(deal, sort_keys=True, indent=2, ensure_ascii=False)
            return log_mess
            
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
    
    # Заберем сделки из СРМ по фильтру
    e, lst_deal = get_deals_crm(pv_crm_code, str(from_date), str(to_date))
    # Догрузим сделки из СРМ по фильтру РТК ОнЛайм
    e2, lst_deal2 = get_deals_crm(25, str(from_date), str(to_date))
    e += e2
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
    log_mess += f'\nПВ {provider}: Исходный список2: {len(lst_deal2)} шт.'
    logger.info(log_mess); print(log_mess)
    
    # Соберем нормальный список сделок
    new_lst_deal = [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal]
    new_lst_deal += [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal2 if dl.get('UF_CRM_5903C16BB2F06') != 'Москва']
    log_mess = f'ПВ {provider}: Нормализованный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    # print(json.dumps(new_lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    # with open('lst_dealRTK.json', 'w', encoding='utf-8') as out_file:
        # json.dump(new_lst_deal, out_file, ensure_ascii=False, indent=4)
    
    # Проверим статус сделок у ПВ
    e, lst_deal = get_deal_status(logger, new_lst_deal, access, status_for_comment)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    if e: 
        log_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return
    
    change = 0
    for deal in lst_deal:
        status = deal.get('pv_status')
        if status and status in status_rtk_srm:
            print(deal.get('ID'), status, name_status_crm[status_rtk_srm[status]])
            deal['crm_status'] = status_rtk_srm[status]
            e = send_crm_deal_stage(deal, deal['crm_status'])
            # e = False
            if e: 
                log_mess = f'ПВ {provider}: Ошибка при обновлении статуса сделки в срм: {e}'
                logger.info(log_mess); print(log_mess)
                send_telegram(tlg_chat, tlg_token, log_mess)
            else: change += 1
            time.sleep(0.5)
    
    e = send_dj_domconnect_result(logger, lst_deal)
    if e:
        log_mess = f'ПВ {provider}: Ошибка при архивировании сделки в dj_domconnect: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)

    tlg_mess = f'ПВ {provider}:\nСтатус сделок изменен\nв {change} из {len(lst_deal)}\n'
    str_today = datetime.today().strftime('%d.%m.%Y')
    tlg_mess += f'http://django.domconnect.ru/api/get_pv_result/{pv_dc_code}/{str_today}'
    
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
    
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 20)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN, 1)
    run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)
    
    # lst_deal = []
    # # # lst_deal.append({'ID': '157942', 'num': '1100298394828'})
    # # lst_deal.append({'ID': '157942', 'num': '1100298314608'})
    # # lst_deal.append({'ID': '157942', 'num': '1100298316713'})
    # # lst_deal.append({'ID': '157942', 'num': '1100298319222'})
    # # lst_deal.append({'ID': '157942', 'num': '1100298319853'})
    # # lst_deal.append({'ID': '157942', 'num': '1100298320393'})
    # lst_deal.append({'ID': '157942', 'num': '1100298323415'})
    # lst_deal.append({'ID': '157942', 'num': '1100298338821'})
    # lst_deal.append({'ID': '157942', 'num': '1100298344326'})
    # lst_deal.append({'ID': '157942', 'num': '1100298364445'})
    # lst_deal.append({'ID': '157942', 'num': '1100298365345'})
    # e, lst_deal = get_deal_status(lst_deal, access, status_for_comment)
    # if e: print(e)
    
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    
    # if lst_deal[0]['status'] == 'Заявка не найдена':
        # print(status_rtk_srm[lst_deal[0]['status']])

    pass