import requests, json, time, logging
from datetime import datetime, timedelta


def send_crm():
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/timeman.status'
    # url = 'https://crm.domconnect.ru/rest/timeman.status'
    
    # Данные для СРМ
    # 'available_connect': '',
    # 'tarifs_all': '',
    # 'pv_address': '',
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    
    params = {
        'auth': '',
        'user_id': 1,  # вся инфа 21888 ??? 11395
    }

    resp = requests.post(url, headers=headers, params=params)
    print(resp.status_code)
    print(resp.text)
    # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/


if __name__ == '__main__':
    send_crm()

