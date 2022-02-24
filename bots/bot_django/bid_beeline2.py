import os
import time
from datetime import datetime
import requests  # pip install requests
import json

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def set_bid(data):
    try:
        base_url = 'https://mk.beeline.ru/PartnProg/RefLink?key=AD8AE6EF4C084ED1'
        url_post = 'https://mk.beeline.ru/PartnProg/RefLinkSendForm'
        user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mk.beeline.ru',
            'Origin': 'https://mk.beeline.ru',
            'Pragma': 'no-cache',
            'Referer': 'https://mk.beeline.ru/PartnProg/RefLink?key=AD8AE6EF4C084ED1',
            'User-Agent': user_agent_val,
            'X-Requested-With': 'XMLHttpRequest',
        }
        session = requests.Session()
        responce = session.get(base_url, headers=headers)
        if responce.status_code != 200: raise Exception(f'Ошибка get ответа сервера билайн {responce.status_code}')
        session.headers.update({'Referer':base_url})
        session.headers.update({'User-Agent':user_agent_val})
        
        i_ph = data.get('phone')
        if not i_ph.isdigit() or len(i_ph) != 11: raise Exception('Ошибка в номере телефона')
        phone = f'+7 ({i_ph[1:4]}) {i_ph[4:7]}-{i_ph[7:9]}-{i_ph[9:11]}'
        print(phone)

        form_data = {
            'client_inn': data.get('client_inn'),
            'contact_name': data.get('contact_name'),
            'phone': phone,
            'email': data.get('email'),
            'dsc': data.get('comment'),
            'client_name': data.get('client_name'),
            'products': data.get('products'),
            'parther_key': data.get('parther_key'),
        }
        responce = session.post(url_post, headers=headers, data=form_data)
        if responce.status_code == 200:
            data['bid_number'] = responce.text
        else: raise Exception(f'Ошибка post ответа сервера билайн {responce.status_code}')

        # data['bid_number'] = '1111'
        # print(responce.status_code)
        # print(responce.text)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(responce.text)

    except Exception as e:
        return e, data, 
   
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
    set_bid_to_dj_domconnect()
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
    
    
    # data = {
        # 'parther_key': 'AD8AE6EF4C084ED1',
        # 'client_inn': '7604350152',
        # 'client_name': 'ООО "Домконнект"',
        # 'contact_name': 'Тестовый Тест Тестович',
        # 'phone': '79991234567',
        # 'email': '',
        # 'dsc': 'Тестовая заявка, просьба не обрабатывать',
        # 'products': 'Интернет',
    # }
    # set_bid(data)
    pass
