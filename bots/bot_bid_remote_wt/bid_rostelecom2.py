import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'


def set_bid(data):
    driver = None
    try:
        base_url = 'https://client.rt.ru/admin/uniapp'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        # ###################### Login ######################
        els = driver.find_elements(By.XPATH, '//input[@name="login-field"]')
        if els[0]: els[0].send_keys(data['login'])
        else: raise Exception('Ошибка авторизации нет поля логин')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="pwd-field"]')
        if els[0]: els[0].send_keys(data['password'])
        else: raise Exception('Ошибка авторизации нет поля пароль')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="login"]')
        if els[0]: els[0].click()
        else: raise Exception('Ошибка авторизации нет кнопки Войти')
        time.sleep(3)
        ###################### Главная страница ######################
        els_btn = driver.find_elements(By.XPATH, '//button[@data-v-6a394f31=""]')
        if len(els_btn) != 1: raise Exception('Нет кнопки добавить')
        els_btn[0].click()
        time.sleep(1)
        
        els_li = driver.find_elements(By.XPATH, '//li[@id="6187630175"]')
        if len(els_li) != 1: raise Exception('Нет элемента меню заявка на подключение')
        els_li[0].click()
        time.sleep(5)
        ###################### Страница ввода заявки ######################
        # Фамилия
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="family"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода фамилии')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода фамилии')
        lastname = data['lastname']
        if len(lastname) < 3: lastname = 'Клиентов'
        els_input[0].send_keys(lastname)
        time.sleep(1)
        # Телефон
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="contact_phone"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода телефона')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода телефона')
        els_input[0].send_keys(data['phone'])
        time.sleep(1)
        # Имя
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="first_name"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода имени')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода имени')
        firstname = data['firstname']
        if len(firstname) < 3: firstname = 'Клиент'
        els_input[0].send_keys(firstname)
        time.sleep(1)
        # Отчество
        patronymic = data['patronymic']
        if patronymic:
            els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="surname"]')
            if len(els_div) != 1: raise Exception('Нет блока ввода отчества')
            els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
            if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода отчества')
            els_input[0].send_keys(patronymic)
            time.sleep(1)
        # Адрес
        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, 500)')
        time.sleep(1)

        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="address"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода адреса')
        els_section = els_div[0].find_elements(By.TAG_NAME, 'section')
        if len(els_section) != 1: raise Exception('Ошибка поиска секции меню адреса')
        els_section[0].click()
        
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода адреса')
        els_input[0].send_keys(data['address'])
        time.sleep(5)
        els_li = els_div[0].find_elements(By.TAG_NAME, 'li')
        if len(els_li) > 0: els_li[0].click()
        time.sleep(1)
        # ИНН/Организация
        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)

        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="organization_name"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода ИНН/Организация')
        els_input = els_div[0].find_elements(By.TAG_NAME, 'input')
        if len(els_input) != 1: raise Exception('Ошибка поиска поля ввода ИНН/Организация')
        els_input[0].send_keys(data['inn_organisation'])
        time.sleep(5)
        els_span = els_div[0].find_elements(By.TAG_NAME, 'span')
        if len(els_span) > 0: els_span[0].click()
        time.sleep(1)
        # Дополнительная информация
        els_div = driver.find_elements(By.XPATH, '//div[@data-qaid="additionalInfo"]')
        if len(els_div) != 1: raise Exception('Нет блока ввода дополнительной информации')
        els_textarea = els_div[0].find_elements(By.TAG_NAME, 'textarea')
        if len(els_textarea) != 2: raise Exception('Ошибка поиска поля ввода дополнительной информации')
        dop_info = f'Адрес: {data["address"]}\n'
        comment =  data['comment']
        if comment: dop_info += f'{comment}\n'
        dop_info += f'Услуга: {data["service"]}\n'
        els_textarea[0].send_keys(dop_info)
        time.sleep(1)
        
        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        # Кнопка далее
        els_btn = driver.find_elements(By.XPATH, '//button[@data-qaid="next_button_service"]')
        if len(els_btn) != 1: raise Exception('Нет кнопки далее')
        disabled = els_btn[0].get_attribute('disabled')
        if disabled == 'true':
            mess = ('После заполнения заявки кнопка Далее не активна.\n'
            f'Возможно не корректен адрес: {data["address"]}\n'
            f'или организация: {data["inn_organisation"]}')
            raise Exception(mess)
        else: els_btn[0].click()
        # Страница добавления услуг
        # Ищем кнопку + интернет
        el_inet_plus = driver.find_element(By.XPATH, '//*[@id="6144362978"]/div/table/tbody/tr/td/div/order-connection/div/div[2]/section/div[1]/div[2]/div/div[3]/div/span[2]')
        el_inet_plus.click()
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
        print(answer)
        lst_answer = answer.split()
        if len(lst_answer) != 4: raise Exception(f'Неивестный формат ответа регистрации заявки {answer}')
        data['bid_number'] = lst_answer[2]
        # print(data['bid_number'])
        
        # time.sleep(10)

        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        
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
        'key': 'Q8kGM1HfWz',
        'login': 'mos.domconnect@gmail.com',
        'password': 'bvo[7dGr',
        'id_lid': '1163386',
        'firstname': 'андрей',
        'patronymic': '',
        'lastname': '',
        'phone': '79111234567',
        'address': 'Ярославль Попова д.22',
        'inn_organisation': '7604350441',
        'service': 'Интернет',
        'comment': 'Тестовая заявка, просьба не обрабатывать',
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
    
    # data = {'id': 1,}
    # set_bid_status(3, data)
    
    # rez, bid_list = get_did_in_dj_domconnect()
    # print(bid_list)
    # data = {
        # 'login': 'mos.domconnect@gmail.com',
        # 'password': 'bvo[7dGr',
        # 'id_lid': '1163386',
        # 'firstname': 'Иван',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79111234567',
        # 'address': 'Ярославль Попова д.22',
        # 'inn_organisation': '7604350441',
        # 'service': 'Интернет',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',
    # }
    # rez, data = set_bid(data)
    # if rez: print(rez)
    
    
