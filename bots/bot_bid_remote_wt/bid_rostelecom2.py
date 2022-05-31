import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'


def set_bid(data):
    driver = None
    try:
        base_url = 'https://client.rt.ru/admin/uniapp'
        
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        # ###################### Login ######################
        els = driver.find_elements(By.XPATH, '//input[@name="login-field"]')
        if els[0]: 
            try: els[0].send_keys(data['login'])
            except: raise Exception('Ошибка действий 1')
        else: raise Exception('Ошибка авторизации нет поля логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="pwd-field"]')
        if els[0]:
            try: els[0].send_keys(data['password'])
            except: raise Exception('Ошибка действий 2')
        else: raise Exception('Ошибка авторизации нет поля пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="login"]')
        if els[0]:
            try: els[0].click()
            except: raise Exception('Ошибка действий 3')
        else: raise Exception('Ошибка авторизации нет кнопки Войти')
        time.sleep(3)
        ###################### Главная страница ######################
        els_btn = driver.find_elements(By.XPATH, '//button[@data-v-6a394f31=""]')
        if len(els_btn) != 1: raise Exception('Нет кнопки добавить')
        try: els_btn[0].click()
        except: raise Exception('Ошибка действий 4')
        time.sleep(1)
        
        els_li = driver.find_elements(By.XPATH, '//li[@id="6187630175"]')
        if len(els_li) != 1: raise Exception('Нет элемента меню заявка на подключение')
        try: els_li[0].click()
        except: raise Exception('Ошибка действий 5')
        time.sleep(10)
        ###################### Страница ввода заявки ######################
        # Фамилия
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="family"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода фамилии')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода фамилии')
        lastname = data['lastname']
        if len(lastname) < 3: lastname = 'Клиентов'
        els_input[0].send_keys(lastname)
        time.sleep(3)
        # Телефон
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="contact_phone"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода телефона')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода телефона')
        els_input[0].send_keys(data['phone'])
        time.sleep(3)
        # Имя
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="first_name"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода имени')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода имени')
        firstname = data['firstname']
        if len(firstname) < 3: firstname = 'Клиент'
        els_input[0].send_keys(firstname)
        time.sleep(3)
        # Отчество
        patronymic = data['patronymic']
        if patronymic:
            els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="surname"]')
            if len(els_div) != 1: raise Exception('Нет блока ввода отчества')
            els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
            if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода отчества')
            els_input[0].send_keys(patronymic)
            time.sleep(3)

        # Адрес
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="address"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода адреса')
        els_section = els_div[0].find_elements(By.TAG_NAME, 'section')
        if len(els_section) != 1: raise Exception('Ошибка поиска секции меню адреса')
        els_section[0].click()
        time.sleep(2)
        
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода адреса')
        
        # Соберем строку адреса
        lst_input_address = []
        lst_comment_address = []
        region = data.get('region')
        if region:
            lst_comment_address.append(region)
            lst_input_address.append(region)
        city = data.get('city')
        if region == None and city:
            lst_input_address.append(city)
        if city:
            lst_comment_address.append(city)
        street = data.get('street')
        if street:
            lst_comment_address.append(street)
        house = data.get('house')
        if house:
            lst_comment_address.append(f'д.{house}')
        apartment = data.get('apartment')
        if apartment:
            lst_comment_address.append(apartment)
        input_address = ' '.join(lst_input_address)
        comment_address = ' '.join(lst_comment_address)
        data['address'] = input_address
        
        els_input[0].send_keys(input_address)
        time.sleep(5)
        els_li = els_div[0].find_elements(By.TAG_NAME, 'li')
        if len(els_li) > 0: els_li[0].click()
        time.sleep(3)

        # ИНН/Организация
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="organization_name"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода ИНН/Организация')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода ИНН/Организация')
        els_input[0].send_keys('ИП')
        time.sleep(3)

        # Дополнительная информация
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="additionalInfo"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода дополнительной информации')
        els_textarea = els_div[0].find_elements(By.TAG_NAME, 'textarea')
        if len(els_textarea) != 2: raise Exception('Ошибка поиска поля ввода дополнительной информации')
        dop_info = f'Адрес: {comment_address}\n'
        comment =  data['comment']
        if comment: dop_info += f'{comment}\n'
        dop_info += f'Услуга: {data["service"]}\n'
        els_textarea[0].send_keys(dop_info)
        time.sleep(3)

        # Кнопка далее
        els_btn = driver.find_elements(By.XPATH, '//button[@data-qaid="next_button_service"]')
        if len(els_btn) != 1: raise Exception('Нет кнопки далее')
        disabled = els_btn[0].get_attribute('disabled')
        
        # time.sleep(20)
        # raise Exception('Finish')
        
        
        if disabled == 'true':
            mess = (f'Адрес: {input_address}\nНе распознан')
            raise Exception(mess)
        else: els_btn[0].click()
        time.sleep(5)
        # Страница добавления услуг
        # Ищем кнопку + интернет
        els_div = driver.find_elements(By.XPATH, '//div[@class="order-connection__ServiceSelection__row order-connection__ServiceSelection__rowServices order-connection__ServiceSelection__w352"]')
        f_ok = False
        for el_div in els_div:
            els_p = el_div.find_elements(By.TAG_NAME, 'p')
            if len(els_p) < 1: continue
            service = els_p[0].get_attribute('innerHTML')
            if service.find('Интернет') >= 0:
                els_plus = el_div.find_elements(By.XPATH, './/span[@class="order-connection__Counter__plus"]')
                if len(els_plus) < 1: raise Exception('Нет кнопки добавить услугу')
                els_plus[0].click()
                f_ok = True
        if f_ok == False: raise Exception('Ошибка добавления услуги интернет')
        time.sleep(1)
        
        # Ищем кнопку Зарегистрировать
        els_btn = driver.find_elements(By.XPATH, '//button[@data-qaid="register_button_service"]')
        if len(els_btn) != 1: raise Exception('Нет кнопки Зарегистрировать')
        disabled = els_btn[0].get_attribute('disabled')
        if disabled == 'true':
            mess = 'После добавления услуг кнопка Зарегистрировать не активна.'
            raise Exception(mess)
        # !!! Внимание, здесь будет отправка заявки !!!
        else: els_btn[0].click()
        time.sleep(3)
        
        # смотрим ответ
        els_div = driver.find_elements(By.XPATH, '//section[@data-v-2f16eb9e=""]')
        if len(els_div) != 1: raise Exception('Нет блока ответа регистрации заявки')
        els_span = els_div[0].find_elements(By.TAG_NAME, 'span')
        if len(els_span) != 1: raise Exception('Нет строки ответа регистрации заявки')
        answer = els_span[0].text
        # print(answer)
        lst_answer = answer.split()
        print(len(answer))
        if len(lst_answer) != 4: raise Exception(answer)
        data['bid_number'] = lst_answer[2]
        print(data['bid_number'])
        
        # time.sleep(10)

        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Finish')
        
    except Exception as e:
        return str(e)[:200], data
    finally:
        if driver: driver.quit()

    return '', data

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_rostelecom2'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        # 'key': 'Q8kGM1HfWz',
        # 'id_lid': '1163386',
        # 'firstname': 'андрей',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79111234567',
        # # 'region': '',
        # 'city': 'Ярославль',
        # 'street': 'Попова',
        # 'house': '24',
        # # 'apartment': '',
        # 'inn_organisation': '7604350441',
        # 'service': 'Интернет',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',
        
        # 'key': 'Q8kGM1HfWz',
        # 'id_lid': '1451113',
        # 'firstname': 'Любовь',
        # 'patronymic': 'Петровна',
        # 'lastname': '',
        # 'phone': '79529311369',
        # 'city': 'Новосибирск',
        # 'street': 'ул В.Высоцкого',
        # 'house': '39',
        # 'inn_organisation': 'ТСЖ',
        # 'service': 'Интернет',
        # 'comment': '',
        
        'key': 'Q8kGM1HfWz',
        'id_lid': '1450899',
        'firstname': '',
        'patronymic': '',
        'lastname': '',
        'phone': '79999685254',
        'city': 'Москва',
        'street': 'ул Строителей',
        'house': '6',
        'apartment': '6',
        'inn_organisation': 'ООО НУТРИСОЛ КЛИНИКА',
        'service': 'Интернет',
        'comment': '',
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        pass
        print('Error: requests.get')

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_rostelecom2'
    
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

def set_bid_status(status, data):
    url = url_host + 'api/set_bid_rostelecom2_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
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

    number_bid_ctn = f'Заявка: {bid_dict.get("bid_number")}'
    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': number_bid_ctn,
        'fields[UF_CRM_5864F4DA85D5A]': bid_dict.get('service'),
        'fields[UF_CRM_1499386906]': bid_dict.get("login")  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1163386/
    except:
        pass

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

def run_bid_rostelecom2(tlg_chat, tlg_token):
    opsos = 'Ростелесом2'
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, bid_list = get_did_in_dj_domconnect()
    if rez:
        tlg_mess = 'Ошибка при загрузке заявок из domconnect.ru'
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
        send_crm_bid(data)  # ответ в CRM
        tlg_mess = ''
        if rez == '':  # заявка успешно создана
            set_bid_status(3, data)
            tlg_mess = f'{opsos}: - создана заявка\n'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = f'{opsos}:\n'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Адрес: {data.get("address")}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================

if __name__ == '__main__':
    # https://client.rt.ru/admin/uniapp
    # mos.domconnect@gmail.com
    # bvo[7dGr
    pass
    # set_did_to_dj_domconnect()
    
    # data = {'id': 1941,}
    # set_bid_status(0, data)
    
    # rez, bid_list = get_did_in_dj_domconnect()
    # if rez: print(rez)
    # print(bid_list)
    
    
    # data = {
        # 'login': 'mos.domconnect@gmail.com',
        # 'password': 'bvo[7dGr',
        # 'id_lid': '1163386',
        # 'firstname': '',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79127549060',
        # 'region': 'Удмуртская Республика',
        # 'city': 'посёлок Игра',
        # 'street': 'Труда',
        # 'house': '8',
        # 'apartment': '',
        # 'inn_organisation': 'ООО Игринская типография',
        # 'service': 'Интернет',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',
    # }
    # rez, data = set_bid(data)
    # if rez: print(rez)
    
    # http://django.domconnect.ru/api/set_bid_rostelecom2?key=Q8kGM1HfWz
    # Клиентов
    # Клиент
    # Удмуртская Республика посёлок Игра
    # ИП
    # Ярославская область Ярославль
