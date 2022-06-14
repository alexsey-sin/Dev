import os, time, json, requests, logging  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

opsos = 'Билайн2'

def set_bid(data):
    driver = None
    try:
        parther_key = data.get('parther_key')
        base_url = f'https://mk.beeline.ru/PartnProg/RefLink?key={parther_key}'

        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        els_inet = driver.find_elements(By.XPATH, '//input[contains(@onclick, "Интернет")]')
        if len(els_inet) < 2: raise Exception('Ошибка нет кнопки Интернет')
        try: els_inet[1].click()
        except: raise Exception('Ошибка действий 1')
        time.sleep(2)
        
        # Поля ИНН и Название компании не обязательные
        # inn = data.get('client_inn')
        # if inn and inn.isdigit() and (len(inn) == 10 or len(inn) == 12):
            # els = driver.find_elements(By.XPATH, '//input[@id="Inn"]')
            # if len(els) != 1: raise Exception('Ошибка нет поля ИНН')
            # try: els[0].send_keys(inn)
            # except: raise Exception('Ошибка действий 2')
            # time.sleep(1)
        
        # client_name = data.get('client_name')
        # if client_name:
            # els = driver.find_elements(By.XPATH, '//input[@id="ClientName"]')
            # if len(els) != 1: raise Exception('Ошибка нет поля Название компании')
            # try: els[0].send_keys(client_name)
            # except: raise Exception('Ошибка действий 3')
            # time.sleep(1)
        
        contact_name = data.get('contact_name')
        if contact_name == None or len(contact_name) < 3: raise Exception('Ошибка не задан ФИО контактного лица')
        els = driver.find_elements(By.XPATH, '//input[@id="ContactName"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ФИО')
        try: els[0].send_keys(contact_name)
        except: raise Exception('Ошибка действий 4')
        time.sleep(3)
        
        i_ph = data.get('phone')
        if not i_ph.isdigit() or len(i_ph) != 11: raise Exception('Ошибка в номере телефона')
        # phone = f'+7 ({i_ph[1:4]}) {i_ph[4:7]}-{i_ph[7:9]}-{i_ph[9:11]}'
        els = driver.find_elements(By.XPATH, '//input[@id="PhoneNumberALL"]')
        if len(els) != 1: raise Exception('Ошибка нет поля Телефон')
        try: els[0].send_keys(i_ph[1:])
        except: raise Exception('Ошибка действий 5')
        time.sleep(3)

        comment = data.get('comment')
        if comment:
            els = driver.find_elements(By.XPATH, '//textarea[@id="Dsc"]')
            if len(els) != 1: raise Exception('Ошибка нет поля Комментарий')
            try: els[0].send_keys(comment)
            except: raise Exception('Ошибка действий 6')
            time.sleep(3)
        
        # Проверим нет ли ошибок
        els = driver.find_elements(By.XPATH, '//span[@class="field-validation-error"]')
        if len(els) > 0:
            err_lst = []
            for el in els:
                err_lst.append(el.text)
            raise Exception('\n'.join(err_lst))
        
        # raise Exception('Финиш.')
        
        # Отправляем
        els = driver.find_elements(By.XPATH, '//input[@id="SubmitButton"]')
        if len(els) != 1: raise Exception('Ошибка нет кнопки отправить')
        try:
            els[0].click()
            time.sleep(2)
            els[0].click()
        except: pass
        time.sleep(3)
        
        # Ловим результат
        els = driver.find_elements(By.XPATH, '//span[@id="ResultContent"]')
        if len(els) != 1: raise Exception('Ошибка нет ответа на заявку')
        ans_txt = els[0].text
        ok_titul = 'Ваша заявка принята под номером'
        if ans_txt.find(ok_titul) >= 0:
            data['bid_number'] = ans_txt.replace(ok_titul, '').strip()
        else: data['bot_log'] = ans_txt
        time.sleep(1)
        
        # time.sleep(5)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)

    except Exception as e:
        # print(e)
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
        'id_lid': '1163386',
        'client_inn_name': '7604350152/ООО "Домконнект"',
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

def run_bid_beeline2(tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    rez, bid_list = get_bid_in_dj_domconnect()
    if rez:
        tlg_mess = f'{opsos}: Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(bid_list) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {opsos}: Заявок нет')
        return

    # Перелистываем список словарей с заявками
    for bid_dict in bid_list:
        rez, data = set_bid(bid_dict)
        data['bot_log'] = rez
        crm = send_crm_bid(data)  # ответ в CRM
        if len(crm) > 0: data['bot_log'] += crm
        if rez == '':  # заявка успешно создана
            set_bid_status(3, data)
            tlg_mess = f'{opsos}: - создана заявка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = f'{opsos}: - ошибка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
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

    # run_bid_beeline2(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    
    
    
    # set_bid_to_dj_domconnect()
    # time.sleep(1)
    # run_bid_beeline2()
    
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
    # data = {
        # 'parther_key': 'AD8AE6EF4C084ED1',
        # 'client_inn': 'ИНН  7734446063',
        # 'client_name': 'ООО ДокДети Октябрьское поле',
        # 'contact_name': 'Светлана',
        # 'phone': '79169012390',
        # 'email': '',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',
        # 'products': 'Интернет',
        
        
        # # 'parther_key': 'AD8AE6EF4C084ED1',
        # # 'client_inn': '6678062975',
        # # 'client_name': 'ООО &quot;Куб&quot',
        # # 'contact_name': 'Слава',
        # # 'phone': '79965913841',
        # # 'email': '',
        # # 'dsc': '',
        # # 'products': 'Интернет',
    # }
    # e, rez = set_bid(data)
    # if e:
        # print(e)
        # exit(0)
    # print('rez:\n', data)
    
    
    pass
