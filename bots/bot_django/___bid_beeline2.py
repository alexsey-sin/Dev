import os, time, json, requests, logging  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def set_bid(data):
    driver = None
    try:
        parther_key = data.get('parther_key')
        base_url = f'https://mk.beeline.ru/PartnProg/RefLink?key={parther_key}'

        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        
        
        # url_post = 'https://mk.beeline.ru:443/PartnProg/RefLinkSendForm'
        # user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'

        # i_ph = data.get('phone')
        # if not i_ph.isdigit() or len(i_ph) != 11: raise Exception('Ошибка в номере телефона')
        # phone = f'+7 ({i_ph[1:4]}) {i_ph[4:7]}-{i_ph[7:9]}-{i_ph[9:11]}'
        # # print(phone)

        # form_data = {
            # 'client_inn': data.get('client_inn'),
            # 'contact_name': data.get('contact_name'),
            # 'client_name': data.get('client_name'),
            # 'phone': phone,
            # 'email': data.get('email'),
            # 'dsc': data.get('comment'),
            # 'products': data.get('products'),
            # 'parther_key': parther_key,
        # }

        # headers = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            # 'Cache-Control': 'no-cache',
            # 'Connection': 'keep-alive',
            # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # # 'Content-Length': str(len(str(form_data))),
            # 'Host': 'mk.beeline.ru',
            # 'Origin': 'https://mk.beeline.ru',
            # 'Pragma': 'no-cache',
            # 'Referer': f'https://mk.beeline.ru/PartnProg/RefLink?key={parther_key}',
            # 'User-Agent': user_agent_val,
            # 'X-Requested-With': 'XMLHttpRequest',
        # }
        # # print(headers)
        # # return '', data,
        
        # session = requests.Session()
        # responce = session.get(base_url, headers=headers)
        # # # responce = session.get(base_url, headers=headers)
        # if responce.status_code != 200: raise Exception(f'Ошибка get ответа сервера билайн {responce.status_code}')
        # session.headers.update({'Referer':base_url})
        # session.headers.update({'User-Agent':user_agent_val})
        # time.sleep(1)
        
        # # responce = session.post(url_post, headers=headers, data=form_data)
        # responce = session.post(url_post, data=form_data)
        
        
        # # responce = session.post(base_url, headers=headers, data=form_data)
        # # responce = requests.post(url_post, data=form_data)
        # # request = requests.Request('POST', url_post, headers=headers, data=form_data)
        # # prepped = session.prepare_request(request)
        # # print(prepped)
        
        
        # if responce.status_code == 200:
            # data['bid_number'] = responce.text
        # # else: raise Exception(f'Ошибка post ответа сервера билайн {responce.status_code}')

        # # data['bid_number'] = '1111'
        # print(responce.status_code)
        # print(responce.text)
        with open('out.html', 'w', encoding='utf-8') as outfile:
            outfile.write(driver.page_source)

    except Exception as e:
        print(e)
        return str(e)[:100], data,
    finally:
        if driver: driver.quit()
    
    return '', data, 

def set_bid_to_dj_domconnect():
    url = url_host + 'api/set_bid_beeline2'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'parther_key': 'AD8AE6EF4C084ED1',
        'client_inn_name': '7604350152/ООО "Домконнект"',
        'id_lid': '1163386',
        'contact_name': 'Тестовый Тест Тестович',
        'phone': '79011111111',
        'email': 'ASinitsin@domconnect.ru',
        'comment': 'Тестовая заявка, просьба не обрабатывать',
        'products': 'Интернет',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        print('Error: requests.get')

def get_bid_in_dj_domconnect():
    url = url_host + 'api/get_bid_beeline2'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        if responce.status_code == 200:
            bid_list = json.loads(responce.text)
            return 0, bid_list
    except:
        return 1, []
    return 2, []

def set_bid_status(status, data):
    url = url_host + 'api/set_bid_beeline2_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
        'ctn_abonent': data.get('ctn_abonent'),
        'bid_number': data.get('bid_number'),
        'status': status,
    }
    bot_log = data.get('bot_log')
    if bot_log:
        params['bot_log'] = bot_log
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        pass

def send_crm_bid(bid_dict):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': bid_dict.get("bid_number"),
        'fields[UF_CRM_1499386906]': '523',
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message
    try:
        responce = requests.post(url, headers=headers, params=params)
        if responce.status_code != 200: return f'Ошибка post ответа сервера CRM {responce.status_code}'
    except:
        return 'Ошибка post запроса сервера CRM'
    # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1163386/
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

def run_beeline2(logger, tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    rez, bid_list = get_bid_in_dj_domconnect()
    if rez:
        tlg_mess = 'bid_beeline2: Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        logger.error(tlg_mess)
        return
    if len(bid_list) == 0:
        logger.info('bid_beeline2: Заявок нет')
        return

    # Перелистываем список словарей с заявками
    for bid_dict in bid_list:
        rez, data = set_bid(bid_dict)
        data['bot_log'] = rez
        crm = send_crm_bid(data)  # ответ в CRM
        if len(crm) > 0: data['bot_log'] += crm
        if rez == '':  # заявка успешно создана
            set_bid_status(3, data)
            tlg_mess = 'Билайн2: - создана заявка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = 'Билайн2: - ошибка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        logger.info(tlg_mess)
        logger.info('TelegramMessage:', r)
        
    #================================================


if __name__ == '__main__':
    # logging.basicConfig(
        # level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
        # filename='log_main.log',
        # datefmt='%d.%m.%Y %H:%M:%S',
        # format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
    # )
    # logger = logging.getLogger(__name__)
    
    # # личный бот @infra
    # TELEGRAM_CHAT_ID = '1740645090'
    # TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    # run_beeline2(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    
    
    
    # set_bid_to_dj_domconnect()
    # time.sleep(1)
    # run_beeline2()
    
    # data = {'id': 1,}
    # set_bid_status(0, data)
    
    # rez, bid_list = get_bid_in_dj_domconnect()
    # set_bid(bid_list[0])
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    
    
    # set_bid_status(2, data)
        # # for k, v in bid_dict.items():
            # # print(f'{k}: {v}')
    # answer = {
        # 'ctn_abonent': '555446987',
        # 'bid_number': '№56632144',
    # }
    # # set_bid_status(4, bid_list[0])

    # # data = {'id': 2,}
    # # set_bid_status(0, data)
    # # rez, bid_list = get_bid_in_dj_domconnect()
    # bid_list[0]['bot_log'] = 'Ошибка при загрузке заявок из domconnect.ru'
    # send_crm_bid(bid_list[0])  # в случае успеха (поля ctn_abonent и bid_number не пустые)
    
    # https://mk.beeline.ru/PartnProg/RefLink?key=AD8AE6EF4C084ED1    
    data = {
        'parther_key': 'AD8AE6EF4C084ED1',
        'client_inn': '7722778272',
        'client_name': 'ОАО  Шуевский текстиль',
        'contact_name': 'Николай',
        'phone': '79050581031',
        'email': '',
        'dsc': '',
        'products': 'Интернет',
        
        
        # 'parther_key': 'AD8AE6EF4C084ED1',
        # 'client_inn': '6678062975',
        # 'client_name': 'ООО &quot;Куб&quot',
        # 'contact_name': 'Слава',
        # 'phone': '79965913841',
        # 'email': '',
        # 'dsc': '',
        # 'products': 'Интернет',
    }
    e, rez = set_bid(data)
    if e:
        print(e)
        exit(0)
    print('rez:\n', data)
    pass
