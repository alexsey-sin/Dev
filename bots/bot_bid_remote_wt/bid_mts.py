import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def find_string_to_substrs(lst: list, substr: str):  # Поиск вхождения подстрок в списке фраз с названиями тарифов, адресов
    '''
        Поиск вхождения подстрок в списке фраз
        Поиск ведется без учера регистра (все приводится к нижнему регистру)
        и проверяется является ли слово самостоятельным.
        Т.е. если подстрока входит в слово частично - поиск неудачен
        На входе список строк lst.
        И строка substr содержащая группу подстрок разделенных ;
        либо просто одна подстрока без разделителей
        Если в списке найдены строки в которых присутствуют
        все подстроки из substr то собирается список кортежей с индексами и фразами
        Если спиок из более 1 значения то перебираем его и выбираем самую
        короткую фразу по длине
        на выходе индекс этой строки в списке
        Если нет вхождения всех подстрок то на выходе -1
    '''
    substr = substr.split(';')
    sub_lst = []
    for x in substr:
        x = x.lower().strip()
        if x != '': sub_lst.append(x)
    
    in_lst = [x.lower().strip() for x in lst]
    
    rez_lst = []
    for i in range(len(in_lst)):  # цикл по списку фраз
        f_ok = True
        for s_sub in sub_lst:  # цикл по подстрокам
            f_sub_ok = False
            i_s = 0
            while 1:
                i_fnd = in_lst[i].find(s_sub, i_s, len(in_lst[i]))
                if i_fnd < 0:
                    f_ok = False
                    break
                else:
                    f_sub_ok_start = False  # Проверка символа перед подстроки
                    f_sub_ok_end = False  # роверка символа после подстроки
                    l_s_sub = i_fnd + len(s_sub)
                    if len(in_lst[i]) == l_s_sub:  # подстрока в конце строки
                        f_sub_ok_end = True
                    else:  # подстрока не в конце строки и следующий символ буква
                        if not in_lst[i][l_s_sub].isalpha():
                            f_sub_ok_end = True
                    if i_fnd == 0: f_sub_ok_start = True
                    elif not in_lst[i][i_fnd-1].isalpha(): f_sub_ok_start = True
                    if f_sub_ok_start and f_sub_ok_end:
                        f_sub_ok = True
                        break
                    
                i_s = i_fnd + len(s_sub)
            if f_sub_ok == False:
                f_ok = False
                break
                
        if f_ok: rez_lst.append((i, in_lst[i]))
    if len(rez_lst) == 1:
        return rez_lst[0][0]
    elif len(rez_lst) > 1:
        l_max = 10000
        i_max = 0
        for tup in rez_lst:
            l_tup = len(tup[1])
            if l_tup < l_max:
                l_max = l_tup
                i_max = tup[0]
        return i_max
    else: return -1

def find_short(f_lst):
    '''
        Поиск самой короткой фразы в списке и выдача её индекса
    '''
    l_min = 10000
    i_min = 0
    for i in range(len(f_lst)):
        l_phr = len(f_lst[i])
        if l_phr < l_min:
            l_min = l_phr
            i_min = i
    return i_min
    
def set_bid(data):
    driver = None
    try:
        base_url = 'https://urmdf.ssl.mts.ru'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'phone')
        if len(els) != 1: raise Exception('Нет поля логин')
        els[0].send_keys(data.get('login'))
        time.sleep(1)

        els = driver.find_elements(By.ID, 'password')
        if len(els) != 1: raise Exception('Нет поля пароль')
        els[0].send_keys(data.get('password'))
        time.sleep(1)

        els = driver.find_elements(By.TAG_NAME, 'button')
        if len(els) != 1: raise Exception('Нет кнопки Войти')
        els[0].click()
        time.sleep(3)
        ###################### Страница поиска адреса ######################
        # Ищем блок для ввода адреса
        els = driver.find_elements(By.XPATH, '//textarea[@data-testid="search"]')
        if len(els) != 1: raise Exception('Ошибка нет строки ввода адреса')

        # Готовим адресную строку
        region = data.get('region')
        if region == None: raise Exception('Ошибка не заполнено поле регион')
        city = data.get('city')
        if city == None: raise Exception('Ошибка не заполнено поле город')
        street = data.get('street')
        if street == None: raise Exception('Ошибка не заполнено поле улица')
        house = data.get('house')
        if house == None: raise Exception('Ошибка не заполнено поле дом')
        # С дробями дома не проходят - откидываем дробь
        house = house.split('/')[0]
        apartment = data.get('apartment')
        if apartment == None: raise Exception('Ошибка не заполнено поле квартира')
        address = f'{region} {city} {street} д. {house} кв. {apartment}'
        # Вводим адрес
        els[0].send_keys(address)
        
        # Возможны 3 варианта ответа
        # 1 нет ТхВ блок <div id="results"> .... Нет технической возможности! Проверьте введенный адрес.</div>
        # 2 Множественный выбор блок <div data-testid="suggestions" ....>
        # 3 Есть возможность блок <div id="results"> с перечнем возможностей
        
        driver.implicitly_wait(1)
        while 1:
            time.sleep(5)
            
            els = driver.find_elements(By.XPATH, '//div[@id="results"]')
            if len(els) == 1:
                if els[0].text.find('Есть возможность подключения') >= 0: break
                if els[0].text.find('Нет технической возможности') >= 0: raise Exception(els[0].text)
            
            # Возможно множественный выбор
            els_m = driver.find_elements(By.XPATH, '//div[@data-testid="suggestions"]')
            if len(els_m) == 1:
                els_btn = els_m[0].find_elements(By.TAG_NAME, 'button')
                if len(els_btn) == 0: raise Exception('Ошибка нет вариантов выбора адреса')
                f_lst = []
                for el_btn in els_btn:
                    f_lst.append(el_btn.text)
                i_fnd = find_short(f_lst)
                driver.execute_script("arguments[0].click();", els_btn[i_fnd])
                continue
            
            raise Exception(f'Ошибка не распознан ответ на адрес {address}')
        
        driver.implicitly_wait(10)
        # Ищем кнопочку перехода
        els = driver.find_elements(By.XPATH, '//button[contains(@class, "SearchInput_Search__SubmitBtn")]')
        if len(els) == 0: raise Exception('Ошибка после адреса нет кнопки активации перехода')
        driver.execute_script("arguments[0].click();", els[0])
        time.sleep(5)
        ###################### Страница тарифных предложений ######################
        els = driver.find_elements(By.XPATH, '//section[contains(@class, "OrderOffers_container")]')
        if len(els) != 1: raise Exception('Ошибка на странице секции тарифов')
        els_art = els[0].find_elements(By.TAG_NAME, 'article')
        if len(els_art) == 0: raise Exception('Ошибка Нет тарифов')
        lst_tar = []
        for el_art in els_art:
            els_n = el_art.find_elements(By.TAG_NAME, 'h4')
            if len(els_n) == 0: raise Exception('Ошибка Нет заголовка тарифа')
            lst_tar.append(els_n[0].text)
            # print(els_n[0].text)
        
        tarif = data.get('tarif')
        if tarif == None: raise Exception('Ошибка не заполнено поле тариф')
        i_fnd = find_string_to_substrs(lst_tar, tarif)
        if i_fnd < 0: raise Exception(f'Ошибка тариф по ключам \"{tarif}\" не найден')
        els_art[i_fnd].click()
        time.sleep(2)
        
        # Нажмем кнопочку перехода
        driver.execute_script('window.scrollTo(0, 0)')  # прокручивает страницу по координатам
        time.sleep(1)
        els_go = driver.find_elements(By.XPATH, '//button[contains(@class, "SearchInput_Search__SubmitBtn")]')
        if len(els_go) != 1: raise Exception('Ошибка Нет кнопки перехода')
        driver.execute_script("arguments[0].click();", els_go[0])
        time.sleep(5)
        # Бывает появляется всплывашка с "Что-то пошло не так"
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//button[contains(@class, "Modal_Modal__ButtonClose")]')
        if len(els) > 0:
            driver.execute_script("arguments[0].click();", els[0])
        driver.implicitly_wait(10)
        
        # Вводим ФИО
        els = driver.find_elements(By.XPATH, '//input[@name="client.name"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода ФИО')
        
        firstname = data.get('firstname', '')
        patronymic = data.get('patronymic', '')
        lastname = data.get('lastname', '')
        fio = f'{firstname} {patronymic} {lastname}'
        if fio.strip() == '': fio = 'Клиент'
        els[0].send_keys(fio)
        time.sleep(1)
        
        # Вводим Телефон
        els = driver.find_elements(By.XPATH, '//input[@name="client.phone"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода телефона')
        phone = data.get('phone')
        if phone == None: raise Exception('Ошибка не задан номер телефона')
        els[0].send_keys(phone[1:])
        time.sleep(1)

        # Вводим доп. информацию
        comment = f'Клиент: {fio}\n'
        comment += f'Адрес: {data["region"]}, {data["city"]}, {data["street"]} д.{data["house"]} кв.{data["apartment"]}\n'
        comment += f'Телефон: {data["phone"]}\n'
        comment += f'Услуга: {tarif}\n'
        comment += f'{data["comment"]}\n'
        els = driver.find_elements(By.XPATH, '//textarea[@placeholder="Комментарий"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода комментария')
        els[0].send_keys(comment)
        time.sleep(1)

        # Ищем кнопку Оформить заявку
        # Старица возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вверх
        driver.execute_script('window.scrollTo(0, -document.body.scrollHeight)')
        time.sleep(1)
        els_bnt = driver.find_elements(By.XPATH, '//button[contains(@class, "ButtonMTS_Button_primary")]')
        if len(els_bnt) != 1: raise Exception('Ошибка нет кнопки Оформить заявку')
        attr_dis = els_bnt[0].get_attribute('disabled')
        if attr_dis: raise Exception('Ошибка кнопка \"Оформить заявку\" не активна')
        # ЗАВЕРШЕНИЕ ВВОДА ЗАЯВКИ!!!!
        els_bnt[0].click()
        time.sleep(10)

        # ###################### Блок результатов заявки ######################
        els_div_rez = driver.find_elements(By.XPATH, '//div[contains(@class, "OrderResult_container")]')
        if len(els_div_rez) != 1: raise Exception('Ошибка нет блока ответа ввода заявки')
        els_rez = els_div_rez[0].find_elements(By.TAG_NAME, 'h2')
        if len(els_rez) == 0: raise Exception('Ошибка нет блока строки ответа ввода заявки')
        if els_rez[0].text.lower().find('ура! удалось оформить') < 0:
            raise Exception(f'Ответ на ввод заявки: {els_rez[0].text}')
        els_div_num = els_div_rez[0].find_elements(By.XPATH, './/div[contains(@class, "OrderResult_order")]')
        if len(els_div_num) != 1: raise Exception('Ошибка нет строки номера заявки')
        num = els_div_num[0].text.split(': ')
        if len(num) == 2:
            data['bid_number'] = num[1]
        else: raise Exception('Ошибка структуры номера заявки')
        els_btn = els_div_rez[0].find_elements(By.TAG_NAME, 'button')
        if len(els_btn) < 2: raise Exception('Ошибка кнопки закрыть блок ответа')
        els_btn[1].click()
        time.sleep(1)
        
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # driver.quit()
        # return '', data
        
        
    except Exception as e:
        print(e)
        return str(e), data,
    finally: driver.quit()   
    
    return '', data, 

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_mts'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'GRYURYEV',
        'password': 'UcoTWY',
        'id_lid': '1163386',
        
        'region': 'Калужская область',         # область или город областного значения
        'city': 'Калуга',           # город
        'street': 'улица Ленина',         # улица
        'house': '31',          # дом
        'apartment': '2',          # квартира

        'tarif': 'ШПД (FTTB) ; ТЛФ (FTTB)', # Название тарифного плана
        'firstname': 'Иван',
        'patronymic': '',
        'lastname': '',
        'phone': '79011111111',
        'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        'bid_number': '',          # номер заявки
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        print('Error: requests.get')

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_mts'
    
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
    url = url_host + 'api/set_bid_mts_status'
    
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

    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': f'Заявка: {bid_dict.get("bid_number")}',
        'fields[UF_CRM_1493413514]': 2,
        'fields[UF_CRM_5864F4DA85D5A]': bid_dict.get('tarif'),
        'fields[UF_CRM_1499386906]': 523  # PartnerWEB
    }
    error_message = bid_dict.get("bot_log")
    if error_message:
        params['fields[UF_CRM_5864F4DAAC508]'] = error_message

    try:
        responce = requests.post(url, headers=headers, params=params)
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

def run_bid_mts(tlg_chat, tlg_token):
    opsos = 'МТС'
    
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
            address = f'{data.get("region")} {data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    pass
    # url: https://urmdf.ssl.mts.ru
    # login: GRYURYEV
    # password: UcoTWY

    # run_bid_mts()
    
    bid_dict = {
        'login': 'GRYURYEV',
        'password': 'UcoTWY',
        'id_lid': '1163386',
        
        'region': 'Калужская область',         # область или город областного значения
        'city': 'Калуга',           # город
        'street': 'улица Ленина',         # улица
        'house': '31',          # дом
        'apartment': '2',          # квартира

        'tarif': 'ШПД (FTTB) ; ТЛФ (FTTB)', # Название тарифного плана
        'firstname': 'Иван',
        'patronymic': '',
        'lastname': '',
        'phone': '79011111111',
        'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        'bid_number': '',          # номер заявки
    }
    
    
    e, data = set_bid(bid_dict)
    if e: print(e)
    
    
    # # print(data['bid_number'])
    # set_did_to_dj_domconnect()
    # rez, bid_list = get_did_in_dj_domconnect()
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    # data = {'id': 2, 'bid_number': '55632145', 'bot_log': 'Заявка принята МТС'}
    # set_bid_status(0, data)
    
    # rez, stre = search_for_an_entry(lst_street, 'Светла')
    # rez = search_for_an_entry(lst_reg, 'ярославль')
    # rez = search_for_an_entry(lst_reg, 'Санкт-Петербург')
    
    
    # print(rez, stre)

    # 'region': 'Ярославская область',         # область или город областного значения
    # 'city': 'Ярославль',           # город
    # 'street': 'проспект Толбухина',         # улица
    # 'house': '31',          # дом
    # 'apartment': '2',          # квартира
    
    # 'region': 'Санкт-Петербург',         # область или город областного значения
    # 'city': 'Санкт-Петербург',           # город
    # 'street': 'улица Маршала Казакова',         # улица
    # 'house': '78к1',          # дом
    # 'apartment': '2',          # квартира

    # Калужская область	Калуга	улица Ленина 31
    # Санкт-Петербург Санкт-Петербург улица Маршала Казакова 78к1
    # Ярославская область Ярославль проспект Толбухина 31



    # partner_login
    # partner_workercode
    # partner_password
    # id_lid
    # city
    # street
    # house
    # apartment
    # firstname
    # lastname
    # phone
    # tarif
    # ctn_abonent
    # bid_number
    # status
    # change_date
    # pub_date

    # lst_reg = [
        # 'респ Адыгея',
        # 'Алтайский край',
        # 'Амурская обл',
        # 'Архангельская обл',
        # 'Астраханская обл',
        # 'респ Башкортостан',
        # 'Белгородская обл',
        # 'респ Бурятия',
        # 'Владимирская обл',
        # 'Волгоградская обл',
        # 'Вологодская обл',
        # 'Воронежская обл',
        # 'Забайкальский край',
        # 'Ивановская обл',
        # 'Иркутская обл',
        # 'респ Калмыкия',
        # 'Калужская обл',
        # 'Камчатский край',
        # 'Кемеровская обл',
        # 'Кировская обл',
        # 'Краснодарский край',
        # 'Красноярский край',
        # 'Курганская обл',
        # 'Курская обл',
        # 'Ленинградская обл',
        # 'Липецкая обл',
        # 'респ Марий Эл',
        # 'Московская обл',
        # 'Нижегородская обл',
        # 'Новгородская обл',
        # 'Новосибирская обл',
        # 'Омская обл',
        # 'Оренбургская обл',
        # 'Орловская обл',
        # 'Пензенская обл',
        # 'Пермский край',
        # 'Приморский край',
        # 'Ростовская обл',
        # 'Рязанская обл',
        # 'Самарская обл',
        # 'г Санкт-Петербург',
        # 'Саратовская обл',
        # 'Свердловская обл',
        # 'Смоленская обл',
        # 'Ставропольский край',
        # 'Тамбовская обл',
        # 'респ Татарстан',
        # 'Тверская обл',
        # 'Томская обл',
        # 'Тульская обл',
        # 'Тюменская обл',
        # 'респ Удмуртская',
        # 'Ульяновская обл',
        # 'Хабаровский край',
        # 'Ханты-Мансийский Автономный округ - Югра АО',
        # 'Челябинская обл',
        # 'Ямало-Ненецкий АО',
        # 'Ярославская обл',
    # ]


    # lst_street = [
        # 'ул Светлая',
        # 'ул Центральная',
    # ]


    
    
    

    
    # data = {'id': 2,}
    # set_bid_beeline_status(0, data)

    # with open('ddd.html', 'w', encoding='utf-8') as f:
        # f.write(responce.text)
    # url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.fields'
        # responce = requests.get(url, headers=headers)
        # print(responce.status_code)
        # print(responce.text)
        # with open('ddd.html', 'w', encoding='utf-8') as f:
            # f.write(responce.text)
        # if responce.status_code == 200:
            # ans = eval(responce.text)
            # result = ans.get('result')
            # print('result:', result)
            # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1163386/
    # set_bid_beeline_status(1, 3, answer)

    # params = {
        # 'id': bid_dict.get('id_lid'),
        # 'fields[UF_CRM_5864F4DAAC508]': '',
        # 'fields[UF_CRM_1493413514]': '',
        # 'fields[UF_CRM_5864F4DA85D5A]': '',
        # 'fields[UF_CRM_1499386906]': '',
    # }

    # set_did_to_dj_domconnect()

    # set_did_to_dj_domconnect()
    # data = {'id': 2, 'bot_log': 'Ошибка парсинга'}
    # set_bid_beeline_status(2, data)
        # # for k, v in bid_dict.items():
            # # print(f'{k}: {v}')
    # answer = {
        # 'ctn_abonent': '555446987',
        # 'bid_number': '№56632144',
    # }
    # # set_bid_beeline_status(4, bid_list[0])

    # # data = {'id': 2,}
    # # set_bid_beeline_status(0, data)
    # # rez, bid_list = get_did_in_dj_domconnect()
    # bid_list[0]['bot_log'] = 'Ошибка при загрузке заявок из domconnect.ru'
    # send_crm_bid(bid_list[0])  # в случае успеха (поля ctn_abonent и bid_number не пустые)
    
    
    pass
