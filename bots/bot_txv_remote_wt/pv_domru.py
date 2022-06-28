import os, time, re, json, logging
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000'
url_host = 'http://django.domconnect.ru'
provider = 'ДомРу'
pv_crm_code = 1  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 2  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

access = {  # Доступы к ПВ
    # 'url': 'https://internet-tv-dom.ru/operator',
    'url': 'https://yar.db.ertelecom.ru/cgi-bin/ppo/es_webface/ds_main.login',
    'login': 'sinitsin',
    'password': 'BVNocturne20'
}
status_domru_srm = {  # Коды статусов: ДомРу = СРМ
    'Заявка выполнена': 2,  # Подключен
    'Заявка отказная': 'NEW',  # Ошибки + коммент
}
name_status_crm = {
    2: 'Подключен',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы ДомРу когда требуется взять коментарий
    'Заявка отказная',
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

        driver.implicitly_wait(20)
        driver.get(access.get('url'))
        time.sleep(3)
        
        ###################### Страница Логин/Пароль ######################
        els = driver.find_elements(By.XPATH, '//input[@name="login$c"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля логин')
        login = access.get('login')
        try: 
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="passwd$c"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля пароль')
        password = access.get('password')
        try: 
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задан пароль')
        except: raise Exception('Ошибка ввода пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика войти')
        time.sleep(5)
        ###################### Страница Фреймы ######################
        # frame name="topframe"
        # frame name="leftframe"
        # frame name="mainFrame"
        # driver.switch_to_default_content()  # вернуться к родительскому кадру
        driver.switch_to.frame('leftframe')  # Загружаем фрейм
        time.sleep(3)
        f_ok = False
        els_a = driver.find_elements(By.TAG_NAME, 'a')
        for el_a in els_a:
            if el_a.text == 'Мои заявки':
                f_ok = True
                try: el_a.click()
                except: raise Exception('Ошибка клика  Мои заявки')
                break
        if f_ok == False: raise Exception('Ошибка Нет ссылки  Мои заявки')
        time.sleep(3)
        
        driver.switch_to.default_content()  # Загружаем родительский фрейм
        time.sleep(1)
        driver.switch_to.frame('mainFrame')  # Загружаем фрейм
        time.sleep(5)
        
        # Отмечаем чек Выбрать все города
        els = driver.find_elements(By.XPATH, '//input[@id="toggle_cities"]')
        if len(els) == 0: raise Exception('Нет кнопки города')
        try: els[0].click()
        except: raise Exception('Ошибка действий 1')
        time.sleep(1)
        
        # Отмечаем чек Выбрать все шаги заявки
        els = driver.find_elements(By.XPATH, '//input[@id="head_cb_id"]')
        if len(els) == 0: raise Exception('Нет кнопки Выбрать все шаги заявки')
        try: els[0].click()
        except: raise Exception('Ошибка действий 2')
        time.sleep(1)
        # Показать
        els = driver.find_elements(By.XPATH, '//input[@id="reqs_btn"]')
        if len(els) == 0: raise Exception('Нет кнопки Выбрать все шаги заявки')
        try: els[0].click()
        except: raise Exception('Ошибка действий 3')
        time.sleep(1)

        # Подождем когда "Проявится" кнопка Показать
        driver.implicitly_wait(1)
        cnt = 600
        while cnt:
            cnt -= 1
            time.sleep(1)
            els = driver.find_elements(By.XPATH, '//input[@id="reqs_btn"]')
            if len(els) == 0: break
            dis = els[0].get_attribute('disabled')
            if dis == None: break
        time.sleep(1)
        driver.implicitly_wait(10)
        
        # Берем таблицу с результатами
        els_tbl = driver.find_elements(By.XPATH, '//table[@id="reqs_tbl"]')
        if len(els_tbl) == 0: raise Exception('Нет таблицы результатов')
        els_bd = els_tbl[0].find_elements(By.TAG_NAME, 'tbody')
        if len(els_bd) == 0: raise Exception('Нет тела таблицы результатов')
        els_tr = els_bd[0].find_elements(By.TAG_NAME, 'tr')
        if len(els_tr) == 0: raise Exception('Нет строк таблицы результатов')
        # Пройдем по строкам и соберем все сделки
        lst_rez = []
        for el_tr in els_tr:
            els_td = el_tr.find_elements(By.TAG_NAME, 'td')
            if len(els_td) != 10: raise Exception('Ошибка структуры таблицы результатов')
            dct = {
                'num': els_td[2].text.strip(),
                'usluga': els_td[4].text.strip(),
                'comment': els_td[5].text.strip(),
                'status': els_td[6].text.strip(),
                'data': els_td[7].text.strip(),
            }
            lst_rez.append(dct)
        
        # проход по всем заявкам
        for deal in lst_deal:
            num = deal.get('num')
            if not num:
                deal['num'] = 'Не определен'
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = 'Номер отсутствует'
                continue
            num = num.strip()
            
            # Проход по полученному списку
            lst_fd = []  # сюда соберем найденные данные
            for rez in lst_rez:
                if num == rez.get('num'): lst_fd.append(rez)
            
            status = ''
            data_connect = ''
            comment = ''
            if len(lst_fd) == 0:
                deal['pv_status'] = 'not_found'
                deal['comment'] = 'Заявка в ЛК не найдена'
                log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("comment", "")}'
                logger.info(log_mess)
                continue
            # Если под этим номером только одна строка
            if len(lst_fd) == 1:
                status = lst_fd[0].get('status')
                data_connect = lst_fd[0].get('data')
                comment = lst_fd[0].get('comment')
            else:
                # print('num', num, 'Услуг:', len(lst_fd))
                # print(json.dumps(lst_fd, sort_keys=True, indent=2, ensure_ascii=False))
                # Проверим нет ли подключенных
                x_stat = ''
                for fd in lst_fd:
                    if x_stat == '': x_stat = fd.get('status')
                    elif x_stat != fd.get('status'): x_stat = 'variable_status'
                    if fd.get('status') == 'Заявка выполнена':
                        status = fd.get('status')
                        data_connect = fd.get('data')
                        break
                if status == '' and x_stat and x_stat != 'variable_status':
                    status = lst_fd[0].get('status')
                    data_connect = lst_fd[0].get('data')
                    comment = lst_fd[0].get('comment')
            if status:
                deal['pv_status'] = status
                if status == 'Заявка выполнена' and data_connect: deal['date_connect'] = data_connect
                if status in status_for_comment and comment: deal['comment'] = comment

            log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("date_connect", "")}|{deal.get("comment", "")}'
            logger.info(log_mess)
        # time.sleep(1)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')


        
        #===========
        # time.sleep(10)
        # print(json.dumps(lst_rez, sort_keys=True, indent=2, ensure_ascii=False))
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


def run_check_deals(logger, tlg_chat, tlg_token, by_days=30):
    logger.info(f'Старт ПВ: {provider}')

    # Определим диапазон дат для фильтра
    cur_date = datetime.today()
    to_date = cur_date.date()
    from_date = (cur_date - timedelta(days=by_days)).date()
    
    # Заберем сделки из СРМ по фильтру
    e, lst_deal = get_deals_crm(pv_crm_code, str(from_date), str(to_date))
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
    new_lst_deal = [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal]
    log_mess = f'ПВ {provider}: Нормализованный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    
    # Проверим статус сделок у ПВ
    e, lst_deal = get_deal_status(logger, new_lst_deal, access, status_for_comment)
    if e: 
        log_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return
    
    change = 0
    for deal in lst_deal:
        status = deal.get('pv_status')
        if status and status in status_domru_srm:
            # print(deal.get('ID'), status, name_status_crm[status_domru_srm[pv_status]])
            deal['crm_status'] = status_domru_srm[status]
            e = send_crm_deal_stage(deal, deal['crm_status'])
            # e = False
            if e: 
                log_mess = f'ПВ {provider}: Ошибка при обновлении статуса сделки в срм: {e}'
                logger.info(log_mess); print(log_mess)
                send_telegram(tlg_chat, tlg_token, log_mess)
            else: change += 1
            time.sleep(0.5)
    e = send_dj_domconnect_result(lst_deal)
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
    
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)
    
    # # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    lst_deal = []
    # # # lst_deal.append({'ID': '157942', 'num': '1100298394828'})
    lst_deal.append({'ID': '157942', 'num': '660028849304'})
    lst_deal.append({'ID': '157942', 'num': '450006671729'})
    send_dj_domconnect_result(lst_deal)
    
    
    # lst_deal.append({'ID': '157942', 'num': '1100298319222'})
    # lst_deal.append({'ID': '157942', 'num': '1100298319853'})
    # lst_deal.append({'ID': '157942', 'num': '1100298320393'})
    e, lst_deal = get_deal_status(logger, lst_deal, access, status_for_comment)
    if e: print(e)
    
    print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    
    # if lst_deal[0]['status'] == 'Заявка не найдена':
        # print(status_rtk_srm[lst_deal[0]['status']])
    # print(get_dc_token())

    pass
    # "pv_code": "1",
    # "id_crm": "1445521",
    # "num_deal": "1456253214578954",
    # "pv_status": "ПВ статус",
    # "crm_status": "Новый СРМ статус1",
    # "date_connect": "date_connect",
    # "comment": "comment"
    
    # Дом.ру
    # Личные кабинеты - разные ссылки. Заходим в ссылку нашего города. 

     # 3. Отчёт кол-во подключенных договоров
     # 4. Ставим даты отчёта
     # 5. Получаем список заявок
     # 6. Если заявки не нашли - ошибка с комментов заявки нет
     # 7. Варианты:
     # 8. В процессе - не трогаем
     # 9. Подключен (и соседняя дата когда подключён)
     # 10. Отказная - в столбике причина отказа берем текст ошибки

    # Есть отчет «мои заявки»
    # Там можно выбрать город

     # 11. Варианты:
     # 12. В процессе - не трогаем
     # 13. Отправить в службу подключения, заявка создана и отложено подключение - в работе
     # 14. Заявка выполнена (и соседняя дата когда подключён)
     # 15. Заявка отказная - в столбике причина отказа берем текст ошибки
     # 16. 


    # Если у нас по номеру 2 заявки (на 2 услуги)
     # 17. Если статус одинаковый  - берем его
     # 18. Если разные статусы - берем то, что подключено
    # Могут быть заявки с _upd - их отсеивать и брать из них номер