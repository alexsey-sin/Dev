import os, time, re, json, logging
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
# from selenium import webdriver  # $ pip install selenium
import undetected_chromedriver as webdriver  # pip install undetected-chromedriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000'
url_host = 'http://django.domconnect.ru'

provider = 'МТС'
pv_crm_code = 2  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 3  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

access = {  # Доступы к ПВ
    'url': 'https://urmdf.ssl.mts.ru/wd/hub',
    'login': 'GRYURYEV',
    'password': 'UcoTWY'
}
status_mts_srm = {  # Коды статусов: МТС = СРМ
    'Успешное подключение': 2,  # Подключен
    'FIX_Отказ.': 'NEW',  # Ошибки + коммент
}
name_status_crm = {
    2: 'Подключен',
    11: 'Служебный',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы МТС когда требуется взять коментарий из истории
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
    # https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.list?
    # order[id]=DESC&filter[>DATE_CREATE]=2022-03-01&filter[UF_CRM_5903C16B84C55]=3&filter[STAGE_ID]=1&filter[UF_CRM_595E343AA0EE2]=0&select[]=UF_CRM_5903C16BDF7A7&select[]=STAGE_ID&select[]=DATE_CREATE&select[]=UF_CRM_595ED493B6E5C
    pass

def wait_spinner(driver):  # Ожидаем спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "LoaderMatrix_container__")]')
        if len(els):
            # print('ju-spinner')
            pass
        else: break
    driver.implicitly_wait(10)
    time.sleep(1)

# =========================================================
def get_deal_status(logger, lst_deal, access, status_for_comment):
    driver = None
    try:
        EXE_PATH = 'driver/chromedriver.exe'

        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)  # , service_log_path='webdriver.log' -- логирование сессии

        driver.implicitly_wait(20)
        driver.get(access.get('url'))
        time.sleep(10)

        ###################### Login ######################
        els = driver.find_elements(By.ID, 'phone')
        if len(els) != 1: raise Exception('Ошибка нет поля логин')
        login = access.get('login')
        try:
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        password = access.get('password')
        try:
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задан пароль')
        except: raise Exception('Ошибка ввода пароль')
        time.sleep(1)

        els = driver.find_elements(By.TAG_NAME, 'button')
        if len(els) != 1: raise Exception('Ошибка нет кнопки войти')
        try: els[0].click()
        except: raise Exception('Ошибка клика войти')
        time.sleep(5)
        ###################### Страница поиска адреса ######################
        wait_spinner(driver)  # Ожидаем спинер
        driver.fullscreen_window()
        # Ищем ссылку на список заявок
        els = driver.find_elements(By.XPATH, '//a[@href="/orders"]')
        if len(els) != 2: raise Exception('Ошибка авторизации или нет ссылки на список заявок')
        try: els[0].click()
        except: raise Exception('Ошибка клика список заявок')
        wait_spinner(driver)  # Ожидаем спинер

        # проход по всем заявкам
        first_pass = True
        num_error = False
        for deal in lst_deal:
            driver.implicitly_wait(5)
            num = deal.get('num').strip()

            if num_error == False:
                # Ищем кнопку ЕЩЁ
                els = driver.find_elements(By.XPATH, '//div[@data-testid="order-list-show-filters"]')
                if len(els) != 1: raise Exception('Ошибка кнопки ЕЩЁ')
                try: els[0].click()
                except: raise Exception('Ошибка клика кнопки ЕЩЁ')
                time.sleep(1)

            els_art = driver.find_elements(By.TAG_NAME, 'article')
            if len(els_art) != 1: raise Exception('Ошибка нет блока фильтр')

            if first_pass:
                # Вводим дату поиска
                els_div = els_art[0].find_elements(By.XPATH, './/div[contains(@class, "OrderFiltersModal_Filter__createdate")]')
                if len(els_div) != 1: raise Exception('Ошибка нет блока createdate')
                els_btn = els_div[0].find_elements(By.XPATH, './/button[@data-testid="date-range-block-toggle"]')
                if len(els_btn) != 1: raise Exception('Ошибка кнопки дата поиска')
                try: els_btn[0].click()
                except: raise Exception('Ошибка клика кнопки раскрытия блока даты')
                time.sleep(2)
                # Определяем начальную дату
                els_dt = els_art[0].find_elements(By.TAG_NAME, 'article')
                if len(els_dt) != 1: raise Exception('Ошибка нет блока дата')
                els_min = els_dt[0].find_elements(By.XPATH, './/button[@data-testid="date-range-calendar-month-minus"]')
                if len(els_min) != 1: raise Exception('Ошибка нет кнопки месяц назад')
                # отмотаем назад 3 месяца
                try:
                    els_min[0].click()
                    time.sleep(0.5)
                    els_min[0].click()
                    time.sleep(0.5)
                    els_min[0].click()
                    time.sleep(0.5)
                except: raise Exception('Ошибка клика листания календаря')
                # Кликаем 1 число
                els_btn = els_dt[0].find_elements(By.XPATH, './/button[@data-testid="date-calendar-choose-day-0"]')
                if len(els_btn) == 0: raise Exception('Ошибка 1 число')
                try: els_btn[0].click()
                except: raise Exception('Ошибка клика кнопки 1 число')
                time.sleep(2)

            # Вводим номер заявки
            els_num = els_art[0].find_elements(By.XPATH, './/input[@data-testid="order-filter-number"]')
            if len(els_num) != 1: raise Exception('Ошибка нет поля номера заявки')
            if first_pass == False:
                try:
                    els_num[0].send_keys(Keys.CONTROL + 'a')
                    time.sleep(0.2)
                    els_num[0].send_keys(Keys.DELETE)
                    time.sleep(0.2)
                except: raise Exception('Ошибка удаления номера заявки')
            try: els_num[0].send_keys(num)
            except: raise Exception('Ошибка ввода номера заявки')
            time.sleep(2)

            # Проверим на ошибки
            driver.implicitly_wait(1)
            els_err = els_art[0].find_elements(By.XPATH, './/span[@data-testid="error-text"]')
            if len(els_err) > 0:
                lst_err = []
                for el_err in els_err:
                    lst_err.append(el_err.text)
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = ', '.join(lst_err)
                num_error = True
                continue

            # Кликаем применить фильтр
            els_aplf = els_art[0].find_elements(By.XPATH, './/button[@data-testid="order-filter-apply"]')
            if len(els_aplf) != 1: raise Exception('Ошибка нет кнопки применить фильтр')
            try: els_aplf[0].click()
            except: raise Exception('Ошибка клика кнопки применить фильтр')
            wait_spinner(driver)  # Ожидаем спинер
            first_pass = False
            num_error = False

            # Смотрим результат
            els_row = driver.find_elements(By.XPATH, '//div[contains(@class, "OrderList_OrderList__Table__Row__")]')
            if len(els_row) == 0:
                deal['pv_status'] = 'not_found'
                deal['comment'] = 'Заявка в ЛК не найдена'
            elif len(els_row) == 1:
                els_td = els_row[0].find_elements(By.XPATH, './/div[contains(@class, "OrderList_OrderList__Table__Row_Item__")]')
                if len(els_td) != 9: raise Exception('Ошибка формата строки таблицы')
                mts_data = els_td[6].text
                mts_comment = els_td[8].text
                deal['pv_status'] = mts_comment
                deal['comment'] = mts_comment
                if mts_comment == 'Успешное подключение': deal['date_connect'] = mts_data
                if mts_comment.find('FIX_Отказ.') >= 0: deal['pv_status'] = 'FIX_Отказ.'
            else:
                deal['pv_status'] = f'many_rows {len(els_row)}'
                deal['comment'] = 'несколько заявок по 1 номеру'
            log_mess = f'ПВ {provider}: {deal["ID"]}|{num}|{deal.get("pv_status", "")}|{deal.get("date_connect", "")}|{deal.get("comment", "")}'
            logger.info(log_mess)

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

    log_mess = f'ПВ {provider}: Исходный список: {len(lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))

    # Соберем нормальный список сделок
    new_lst_deal = [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal]
    log_mess = f'ПВ {provider}: Нормализованный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)

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
        if status and status in status_mts_srm:
            # print(deal.get('ID'), status, name_status_crm[status_mts_srm[status]])
            deal['crm_status'] = status_mts_srm[status]
            # e = send_crm_deal_stage(deal, deal['crm_status'])
            e = False
            if e:
                log_mess = f'ПВ {provider}: Ошибка при обновлении статуса сделки в срм: {e}'
                logger.info(log_mess); print(log_mess)
                send_telegram(tlg_chat, tlg_token, log_mess)
            else: change += 1
            time.sleep(0.5)

    # e = send_dj_domconnect_result(lst_deal)
    # if e:
        # log_mess = f'ПВ {provider}: Ошибка при архивировании сделки в dj_domconnect: {e}'
        # logger.info(log_mess); print(log_mess)
        # send_telegram(tlg_chat, tlg_token, log_mess)

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

    run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)
    # access = {  # Доступы к ПВ
        # 'url': 'https://urmdf.ssl.mts.ru/wd/hub',
        # 'login': 'GRYURYEV',
        # 'password': 'UcoTWY'
    # }

    # lst_deal = []
    # lst_deal.append({'ID': '142632', 'num': '1-729819687456'})
    # lst_deal.append({'ID': '142884', 'num': '1'})
    # lst_deal.append({'ID': '142632', 'num': '1-729822687456'})
    # lst_deal.append({'ID': '142884', 'num': '1'})
    # lst_deal.append({'ID': '142632', 'num': '1-729819687336'})
    # # lst_deal.append({'ID': '143114', 'num': '1'})
    # e, lst_deal = get_deal_status(logger, lst_deal, access, status_for_comment)
    # if e: print(e)

    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))


    pass