import os
import time
from datetime import datetime
import requests  # pip install requests
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import json

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def set_bid_status(id, status):
    # url = 'http://127.0.0.1:8000/api/set_bid_domru2_status'
    url = 'http://django.domconnect.ru/api/set_bid_domru2_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'id': id,
        'status': status,
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        pass

def get_bid_in_dj_domconnect():
    # url = 'http://127.0.0.1:8000/api/get_bid_domru2'
    url = 'http://django.domconnect.ru/api/get_bid_domru2'
    
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
    except:
        return 1, []
    if responce.status_code == 200:
        bid_list = json.loads(responce.text)
        return 0, bid_list
    return 2, []

def get_form_sample():
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    url = 'https://dealers.dom.ru/request/widget'
    headers = {
        'Referer': 'https://dealers.dom.ru/',
        'User-Agent': user_agent_val,
    }
    params = {
        'domain': 'yar',
        'referral_id': '1000096145',
    }
    try:
        responce = requests.get(url, headers=headers, params=params)
        content = responce.text
    except:
        return 1, {}
    if responce.status_code != 200:
        return 2, {}

    #=================================
    # # print(resp.status_code)
    # # with open('form_sample.html', 'w', encoding='utf-8') as f:
        # # f.write(content)
    #=================================
    # with open('form_sample.html', 'r', encoding='utf-8') as f:
        # content = f.read()
    #=================================
    
    bs_content = BeautifulSoup(content, 'html.parser')
    
    els_option = bs_content.find_all('option')
    out_dict = {}
    for el_option in els_option:
        out_dict[el_option.text] = el_option['value']
    
    return 0, out_dict

def get_street():
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    session = requests.Session()
    url = 'https://dealers.dom.ru/request/widget'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    params = {
        'domain': 'yar',
        'referral_id': '1000096145',
    }
    data = {
        'city': 'yar',  # попставняется из value
        'term': 'ленина',  # начало адрева в нижнем регистре
    }
    # https://dealers.dom.ru/request/widget?domain=yar&referral_id=1000096145
    url += '/request/default/streets'
    resp = session.get(url, headers=headers, params=params, data=data)
    session.headers.update({'Referer':url})
    session.headers.update({'User-Agent':user_agent_val})

    print(resp.status_code)
    print(resp.text)
   
    print(resp.status_code)
    with open('streets', 'w', encoding='utf-8') as f:
        f.write(resp.text)


def set_bid(form):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    session = requests.Session()
    url = 'https://dealers.dom.ru/'
    
    params = {
        'domain': 'yar',
        'referral_id': '1000096145',
    }

    url += 'request/widget'
    resp = session.get(url, headers=headers, params=params)
    session.headers.update({'Referer':url})
    session.headers.update({'User-Agent':user_agent_val})
    
    bs_content = BeautifulSoup(resp.text, 'html.parser')
    
    el_csrf = bs_content.find('meta', attrs={'name': 'csrf-token'})
    csrf = el_csrf['content']  # print(csrf)
    
    form['_csrf'] = csrf
    try:
        resp = session.post(url, headers=headers, params=params, data=form)
        if resp.status_code == 200:
            i = resp.text.find('Заявка отправлена')
            if i < 0:
                return 2
        else:
            return 3
    except:
        return 1
    # print(resp.status_code)
    # print(resp.text)
   
    # with open('answer.html', 'r', encoding='utf-8') as f:
        # html = f.read()
        # i = html.find('Заявка отправлена')
        # if i < 0:
            # return 2
        
    # Заявка отправлена!!!
    return 0
    
    
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
        'fields[UF_CRM_1493413514]': '1',
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

def run_domru2(logger, tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    rez, bid_list = get_bid_in_dj_domconnect()
    if rez:
        tlg_mess = 'ДомРу2: Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        logger.error(tlg_mess)
        return
    if len(bid_list) == 0:
        logger.info('bid_domru2: Заявок нет')
        return

    rez, citys_dict = get_form_sample()
    if rez:
        tlg_mess = 'ДомРу2: Ошибка при загрузке формы dealers.dom.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        logger.error(tlg_mess)
        return
    
    # Перелистываем список словарей с заявками
    for bid_dict in bid_list:
        id_bid = bid_dict.get('id')
        str_city = bid_dict.get('city').strip()
        if str_city not in citys_dict:
            tlg_mess = f'Заявка id {id_bid}: ошибка распознавания города "{str_city}".')
            set_bid_status(bid_dict.get('id'), 3)  # посылаем в домконнект сообщение об ошибке
            send_telegram(tlg_chat, tlg_token, tlg_mess)
            logger.info(tlg_mess)
            # отправляем оператору заявку для ручного ввода
            send_crm_bid(bid_dict)
            continue
          
        var_city = citys_dict[str_city]
        street = bid_dict.get('street').strip()
        house = bid_dict.get('house').strip()
        apartment = bid_dict.get('apartment').strip()
        name = bid_dict.get('name').strip()
        n_ph = bid_dict.get('phone').strip()
        num_phone = f'+7 {n_ph[1:4]} {n_ph[4:7]}-{n_ph[7:9]}-{n_ph[9:]}'
        service_tv = bid_dict.get('service_tv')
        service_net = bid_dict.get('service_net')
        service_phone = bid_dict.get('service_phone')
        
        # comment = 'Тестовая заявка, просьба не обрабатывать.\n' + bid_dict.get('comment')
        comment = f'Адрес клиента: {str_city}, {street}, дом {house}, кв. {apartment}\n'
        if len(bid_dict.get('comment')) > 0:
            comment += f'Комментарий: {bid_dict.get("comment")}'
        # собираем в словарь данных
        form = {
            'WidgetForm[referralId]': '1000096145',
            'WidgetForm[city]': var_city,
            'WidgetForm[street]': street,
            'WidgetForm[streetId]': '1',
            'WidgetForm[house]': house,
            'WidgetForm[houseId]': '1',
            'WidgetForm[flat]': apartment,
            'WidgetForm[name]': name,
            'WidgetForm[phone]': num_phone,
            'WidgetForm[email]': '',
            'WidgetForm[prim]': comment,
            'WidgetForm[internet]': service_net,
            'WidgetForm[tv]': service_tv,
            'WidgetForm[telephony]': service_phone,
        }
        rez = set_bid(form)
        if rez == '':  # заявка успешно создана
            set_bid_status(3, data)
            tlg_mess = 'ДомРу2: - создана заявка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = 'ДомРу2: - ошибка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        logger.info(tlg_mess)
        logger.info('TelegramMessage:', r)
        # if rez:  # если какая-то ошибка
            # set_bid_status(bid_dict.get('id'), 3)  # посылаем в домконнект сообщение об ошибке
            # # glob_rez[bid_dict.get('id')] = 3
            # # отправляем оператору заявку для ручного ввода
            # send_crm_bid(bid_dict)
        # else:
            # set_bid_status(bid_dict.get('id'), 4)  # посылаем в домконнект сообщение об об успешной отправке заявки
            # # glob_rez[bid_dict.get('id')] = 4
        # # r = send_crm_bid(bid_dict)
        # # glob_rez['CRM'] = r

        time.sleep(1)
    #============================================================
    # return glob_rez
    
    
if __name__ == '__main__':
    pass
