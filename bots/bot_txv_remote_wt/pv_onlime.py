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
url_onlime = 'https://dealer.onlime.ru'

provider = 'Онлайм'
pv_crm_code = 25  # http://django.domconnect.ru/admin/domconnect/dccatalogproviderseo/
pv_dc_code = 6  # код по моделям django.domconnect.ru

# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот проверки сделок (ПВ)        PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN
PV_TELEGRAM_CHAT_ID = '-654103882'
PV_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'

# Документация: https://dealer.onlime.ru/beta/apidocs/
access = {  # Доступы к ПВ
    'url': 'https://dealer.onlime.ru',
    'login': 'inetme12',
    'password': 'RxIT9oxP'
}
status_pv_srm = {  # Коды статусов: PV = СРМ
    'Новая': 'NEW',  # Ошибки + коммент
    'Отменена': 'NEW',  # Ошибки + коммент
    'Фин.недозвон': 'NEW',  # Ошибки + коммент
    'Возвращено': 'NEW',  # Ошибки + коммент
    'Ожидание ПТВ': 'NEW',  # Ошибки + коммент
    'Выполнена': 2,  # Подключен
}
name_status_crm = {
    2: 'Подключен',
    'NEW': 'Ошибки',
}
status_for_comment = [  # Статусы когда требуется взять коментарий
    'Новая',
    'Отменена',
    'Фин.недозвон',
    'Возвращено',
    'Ожидание ПТВ',
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
                'UF_CRM_5903C16BB2F06': 'Москва',  # Область
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

def get_token(access):
    url = access.get('url', '') + '/api/dealer/authorize'

    headers = {
        'Content-Type': 'application/json',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    data = {
        'login': access.get('login', ''),
        'password': access.get('password', ''),
    }
    try:
        responce = requests.post(url, headers=headers, json=data)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            if resp_code != 0: return 'Error', f'get_token: resp_code={resp_code}'
            access_token = answer.get('access_token', 'None')
            # expires_in = answer.get('expires_in')
            return '', access_token
        else:
            return f'Ошибка get_token: responce.status_code: {responce.status_code}\n{responce.text}', ''

        # {"resp_code":0,"access_token":"y9Hhze7_eiigdE1xa91-VCjHVgpvFkg8","expires_in":28800}
    except Exception as e:
        return f'Ошибка get_token: try: requests.post {e}', ''

def get_OrderStatus(token, num):
    url = url_onlime + '/api/dealer/order/getorderstatus'
    
    headers = {'Authorization': token}
    params = {'order_id': num}
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            answer = json.loads(responce.text)
            resp_code = answer.get('resp_code')
            orders = answer.get('Orders')
            if resp_code == 0: return '', orders[0]  # норм
            elif resp_code == -1 or resp_code == 1:
                resp_description = answer.get('resp_description')
                return f'Ошибка запроса get_OrderStatus: {resp_description}', []
            else: return f'Ошибка get_OrderStatus: resp_code: {resp_code} не распознан ответ', []
        else:
            return f'Ошибка get_OrderStatus: responce.status_code: {responce.status_code}\n{responce.text}', []
        
    except Exception as e:
        return f'Ошибка get_OrderStatus: try: requests.get: {e}', []

# =========================================================
def get_deal_status(logger, lst_deal, access, status_for_comment):
    try:
        # Получаем токен
        cnt_try = 5
        while cnt_try:
            rez, token = get_token(access)
            if rez == '' and token != 'None': break
            cnt_try -= 1
            print(f'Попытка {5-cnt_try} неудачна')
            time.sleep(5)

        if cnt_try == 0: raise Exception('Ошибка получения токена авторизации')
        time.sleep(0.1)
        # print(token)
        
        # проход по всем заявкам
        for deal in lst_deal:
            num = deal.get('num', 'None')
            l_sub = re.findall('(?:^|\D)1\d{6}(?:\D|$)', str(num))  # (?: начало строки | не цифра) номер с 1 всего 7 знаков (?: конец строки | не цифра)
            if len(l_sub) > 0: num = l_sub[0].strip()
            else:
                deal['pv_status'] = 'deal_number_error'
                deal['comment'] = 'Номер заявки по шаблону не найден'
                continue
            # print('\n', num)
            
            e, ans = get_OrderStatus(token, num)
            if e:
                deal['pv_status'] = 'error_query'
                deal['comment'] = e
                continue
            
            idStatus = ans.get('idStatus')
            if idStatus and idStatus == -1:
                deal['pv_status'] = 'Заявка не найдена'
                deal['comment'] = 'Заявка не найдена'
                continue
            
            # print(json.dumps(ans, sort_keys=True, indent=2, ensure_ascii=False))
            status = ans.get('Status')
            deal['pv_status'] = status
            deal['comment'] = status
            
            if status == 'Выполнена':
                date = ans.get('UpdateDate', '')
                deal['date_connect'] = date
            
            time.sleep(0.2)
        
        # raise Exception('Финиш.')

    except Exception as e:
        return str(e)[:300], lst_deal

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
    if e:
        log_mess = f'ПВ {provider}: загрузка сделок из срм: {e}'
        logger.error(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return
    if len(lst_deal) == 0:
        log_mess = f'ПВ {provider}: Сделок нет'
        logger.info(log_mess); print(log_mess)
        return


    # Соберем список сделок
    new_lst_deal = [{'ID': dl.get('ID'), 'num': dl.get('UF_CRM_5903C16BDF7A7')} for dl in lst_deal]
    log_mess = f'ПВ {provider}: Исходный список: {len(new_lst_deal)} шт.'
    logger.info(log_mess); print(log_mess)
    # print(json.dumps(new_lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    # with open('new_lst_deal.json', 'w', encoding='utf-8') as out_file:
        # json.dump(new_lst_deal, out_file, ensure_ascii=False, indent=4)

    # Проверим статус сделок у ПВ
    e, lst_deal = get_deal_status(logger, new_lst_deal, access, status_for_comment)
    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    if e:
        log_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e}'
        logger.info(log_mess); print(log_mess)
        send_telegram(tlg_chat, tlg_token, log_mess)
        return

    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))
    # with open('new_lst_deal.json', 'w', encoding='utf-8') as out_file:
        # json.dump(lst_deal, out_file, ensure_ascii=False, indent=4)
    
    
    change = 0
    for deal in lst_deal:
        status = deal.get('pv_status')
        if status and status in status_pv_srm:
            print(deal.get('ID'), status, name_status_crm[status_pv_srm[status]])
            deal['crm_status'] = status_pv_srm[status]
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
    if e: tlg_mess += f'\nОшибка архивации: {e}'

    e = send_telegram(tlg_chat, tlg_token, tlg_mess)
    logger.info(tlg_mess.replace('\n', ''))
    logger.info(f'Финиш ПВ: {provider} {e}')


if __name__ == '__main__':
    # Документация: https://dealer.onlime.ru/beta/apidocs/
    # login: inetme12
    # password: RxIT9oxP

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

    run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 3)
    # run_check_deals(logger, PV_TELEGRAM_CHAT_ID, PV_TELEGRAM_TOKEN, 1)
    # run_check_deals(logger, MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)
    # access = {  # Доступы к ПВ
        # 'url': 'https://urmdf.ssl.mts.ru/wd/hub',
        # 'login': 'GRYURYEV',
        # 'password': 'UcoTWY'
    # }

    # lst_deal = []
    # lst_deal.append({'ID': '142632', 'num': '1169958 146999686'})
    # lst_deal.append({'ID': '142884', 'num': '1169753 '})
    # lst_deal.append({'ID': '142632', 'num': '1-729822687456'})
    # lst_deal.append({'ID': '142884', 'num': '1'})
    # lst_deal.append({'ID': '142632', 'num': '1-729819687336'})
    # lst_deal.append({'ID': '143114', 'num': '1'})



    # e, lst_deal = get_deal_status(logger, lst_deal, access, status_for_comment)
    # if e: print(e)

    # print(json.dumps(lst_deal, sort_keys=True, indent=2, ensure_ascii=False))


    pass