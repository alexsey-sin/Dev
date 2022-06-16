import os, time, re, json, logging
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
# import undetected_chromedriver as webdriver  # pip install undetected-chromedriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000'
url_host = 'http://django.domconnect.ru'

provider = 'ТТК'
pv_crm_code = 4  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 5  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

access = {  # Доступы к ПВ
    'url': 'https://onyma-crm.ttk.ru:4443/onyma/',
    'login': 'wd_dc_sg',
    'password': '9zWxQjOh'
}
status_pv_srm = {  # Коды статусов: ТТК = СРМ
    'Работы выполнены': 2,  # Подключен
    'Абонент отказался': 'NEW',  # Ошибки + коммент
}
name_status_crm = {
    2: 'Подключен',
    11: 'Служебный',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы ТТК когда требуется взять коментарий из истории
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

def wait_spinner(driver):  # Ожидаем крутящийся спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//span[@class="loader"]')
        if len(els):
            attr_disp = els[0].get_attribute('style')
            if attr_disp == '':
                print('spinner')
                continue
            else: break
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

def find_link(driver):
    els_div = driver.find_elements(By.XPATH, '//div[@class="group"]')
    for el_div in els_div:
        els_h = el_div.find_elements(By.TAG_NAME, 'h2')
        if els_h and els_h[0].text.strip() == 'WF. Список процессов':
            els_a = el_div.find_elements(By.XPATH, './/a[contains(@href, "/onyma/system/search/locator/?id=")]')
            if len(els_a) > 0:
                for el_a in els_a:
                    if el_a.text.find('[Управление услугами]') >= 0: return el_a

    return None

# =========================================================
def get_deal_status(logger, lst_deal, access, status_for_comment):
    driver = None
    try:
        EXE_PATH = 'driver/chromedriver.exe'

        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)  # , service_log_path='webdriver.log' -- логирование сессии

        base_url = access.get('url')
        driver.get(base_url)
        time.sleep(5)

        ###################### Login ######################
        els = driver.find_elements(By.XPATH, '//input[@id="id_login"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля логин')
        login = access.get('login')
        try:
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задано значение логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@id="id_password"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля пароль')
        password = access.get('password')
        try:
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задано значение пароль')
        except: raise Exception('Ошибка ввода пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//select[@id="id_realm"]')
        if len(els) != 1: raise Exception('Ошибка Нет поля тип пользователя')
        f_ok = False
        els_opt = els[0].find_elements(By.TAG_NAME, 'option')
        for el_opt in els_opt:
            if el_opt.get_attribute('value') == 'ttk':
                try: el_opt.click()
                except: raise Exception('Ошибка клика ТТК')
                time.sleep(1)
                f_ok = True
                break
        if f_ok == False: raise Exception('Ошибка Пользователя ТТК нет в списке')

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка Нет кнопки Войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика Войти')
        time.sleep(5)

        ###################### Страница Главная ######################
        # проход по всем заявкам
        for deal in lst_deal:
            time.sleep(3)
            num = deal.get('num')
            if not num:
                deal['num'] = 'Не определен'
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = 'Номер отсутствует'
                continue
            num = num.strip()

            isok = re.fullmatch(r'^(?:A|А)-\d+', num)
            if not isok:
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = 'Номер не корректен'
                continue

            # Ищем поле поиска
            els_f = driver.find_elements(By.XPATH, '//input[@class="w-text change_inited"]')
            if len(els_f) == 0: raise Exception('нет поля поиска')
            try: 
                els_f[0].send_keys(Keys.CONTROL + 'a')
                time.sleep(0.2)
                els_f[0].send_keys(Keys.DELETE)
                time.sleep(0.2)
                els_f[0].send_keys(num)
            except: raise Exception('Ошибка ввода номера заявки')
            time.sleep(3)

            # Ищем ссылку управления услугами
            el_a = find_link(driver)
            if el_a == None:
                # Отмечаем поиск в истории
                els_ch = driver.find_elements(By.XPATH, '//input[@name="search_in_history"]')
                if len(els_ch) == 0: raise Exception('нет чека истории')
                try: els_ch[0].click()
                except: raise Exception('Ошибка клика чека истории')
                time.sleep(3)
                el_a = find_link(driver)
            
            if el_a == None:
                deal['pv_status'] = 'Заявка не найдена'
                continue
            try: el_a.click()
            except: raise Exception('Ошибка клика ссылки на страницу заявки')
            time.sleep(5)

            # Страница заявки
            # смотрим таблицу в шапке
            els_tbl = driver.find_elements(By.XPATH, '//table[contains(@class, "listtable object-info control")]')
            if len(els_tbl) == 0:
                deal['pv_status'] = 'Ошибка парсинга'
                deal['comment'] = 'Нет сводной таблицы'
                continue
            # Берем статус
            els_s = els_tbl[0].find_elements(By.XPATH, './/td[@data-name="result"]')
            if len(els_s) == 0:
                deal['pv_status'] = 'Ошибка парсинга'
                deal['comment'] = 'Нет ячейки статуса'
                continue
            status = els_s[0].text.strip()
            if status == 'Новый':
                # print(num, 'Новый, пропускаем')
                deal['pv_status'] = 'Новый'
                continue
            elif status != 'Завершен':
                deal['pv_status'] = status
                deal['comment'] = 'Неизвестный статус, пропущено'
                print(num, status, 'Неизвестный статус, пропущено')
                continue
            
            # Берем дату окончания
            els_d = els_tbl[0].find_elements(By.XPATH, './/td[@data-name="end_dt"]')
            if len(els_d) == 0:
                deal['pv_status'] = 'Ошибка парсинга'
                deal['comment'] = 'Нет ячейки даты'
                continue
            deal['date_connect'] = els_d[0].text
            
            # Раскрываем выполненные задачи
            els_a = driver.find_elements(By.XPATH, '//a[contains(@onclick, "Развернуть")]')
            if len(els_a) == 0:
                deal['pv_status'] = 'Ошибка парсинга'
                deal['comment'] = 'Нет ссылки раскрыть'
                continue
            try: els_a[0].click()
            except: raise Exception('Ошибка клика раскрыть')
            time.sleep(1)
            
            # Анализируем таблицу Выполненные задачи
            els_tbl = driver.find_elements(By.XPATH, '//table[@class="flatten"]')
            if len(els_a) == 0:
                deal['pv_status'] = 'Ошибка парсинга'
                deal['comment'] = 'Нет таблицы Выполненные задачи'
                continue
            els_tr = els_tbl[0].find_elements(By.TAG_NAME, 'tr')
            pv_status = ''
            for el_tr in els_tr:
                els_td = el_tr.find_elements(By.TAG_NAME, 'td')
                txt_st = els_td[3].text.strip()
                if txt_st in status_pv_srm:
                    pv_status = txt_st
                    break
            if pv_status == '':
                deal['pv_status'] = 'Завершено'
                deal['comment'] = 'Состояние завершения не определено'
                continue
            deal['pv_status'] = pv_status
            
            # Если отказ смотрим комментарий
            if status_pv_srm[pv_status] == 'NEW':
                els_apr = driver.find_elements(By.XPATH, '//a[@href="#remarks"]')
                if len(els_apr) == 0:
                    deal['comment'] = 'Ошибка: Нет ссылки комментарий'
                    continue
                try: els_apr[0].click()
                except: raise Exception('Ошибка клика комментарий')
                time.sleep(5)
            
                els_note = driver.find_elements(By.XPATH, '//td[(@class="note-body") and (@data-name="note")]')
                if len(els_note) > 0: deal['comment'] = re.sub("\n|\r", ' ', els_note[-1].text)
                else: deal['comment'] = 'Комментарий не найден'
            
            time.sleep(1)
        

        #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        #===========



    except Exception as e:
        return str(e)[:200], lst_deal
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


def run_check_deals(logger, tlg_chat, tlg_token, by_days=60):
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

    # Соберем нормальный список сделок
    new_lst_deal = [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal]
    log_mess = f'ПВ {provider}: Исходный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))

    # Проверим статус сделок у ПВ
    e, lst_deal = get_deal_status(logger, new_lst_deal, access, status_for_comment)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    # with open('lst_deal.json', 'w', encoding='utf-8') as out_file:
        # json.dump(lst_deal, out_file, ensure_ascii=False, indent=4)
    if e:
        log_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return

    change = 0
    for deal in lst_deal:
        status = deal.get('pv_status')
        if status and status in status_pv_srm:
            # print(deal.get('ID'), status, name_status_crm[status_pv_srm[status]])
            deal['crm_status'] = status_pv_srm[status]
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

    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 10)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 3)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)

    # lst_deal = []
    # lst_deal.append({'ID': '142632', 'num': 'А-65771557'})
    # lst_deal.append({'ID': '142884', 'num': 'А-65772345'})
    # lst_deal.append({'ID': '142884', 'num': 'А-65773445'})
    # # lst_deal.append({'ID': '142632', 'num': 'А-657041994555'})
    # # lst_deal.append({'ID': '142632', 'num': 'А-657041994555f'})
    # # # lst_deal.append({'ID': '143114', 'num': '1'})
    # e, lst_deal = get_deal_status(logger, lst_deal, access, status_for_comment)
    # if e: print(e)

    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))


    pass