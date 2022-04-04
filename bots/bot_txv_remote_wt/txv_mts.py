import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'МТС'
pv_code = 3

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
    
def check_equality_citys(lst: list, in_str: str):  # Поиск вхождения фразы в списке фраз
    '''
        Поиск вхождения фразы в списке фраз
        Поиск ведется последовательно начиная с первой буквы in_str
        - назовем её подстрока. Если таких вхождений в списке много,
        2 и более добавляем следующую букву к подстроке.
        Поиск завершен если вхождений только одно.
        Возвращаем индекс фразы в списке и саму фразу.
        Если нет вхождений - возвращаем "-1"
    '''
    # Преобразуем входные данные к нижнему регистру
    in_str = in_str.lower().replace('ё', 'е')
    in_lst = [s.lower().replace('ё', 'е') for s in lst]
    
    ret_ind = -1
    ret_phrase = ''
    # поиск с циклом по набиранию подстроки
    for i_s in range(len(in_str)):
        sub_str = in_str[0:i_s+1]
        cnt_phr = 0
        # просмотрим список на вхождение
        for i_lst in range(len(in_lst)):
            if in_lst[i_lst].find(sub_str) >= 0:
                cnt_phr += 1
                ret_ind = i_lst
        if cnt_phr > 1:
            ret_ind = -1
        else:
            break
    if ret_ind >= 0: return [ret_ind,]  # похожая фраза найдена и она в единственной строке
    
    # просмотрим список на полное совпадение
    ret_ind = -1
    cnt_phr = 0
    for i_lst in range(len(in_lst)):
        if in_lst[i_lst] == in_str:
            cnt_phr += 1
            ret_ind = i_lst
    if cnt_phr == 1: return [ret_ind,]

    # просмотрим список на полное совпадение как самостоятельного слова
    # ret_ind = -1
    # cnt_phr = 0
    ln_sb = len(in_str)
    rez_lst = []
    for i_lst in range(len(in_lst)):
        ln_str = len(in_lst[i_lst])
        i = in_lst[i_lst].find(in_str)
        if i >= 0:
            if in_str == 'омск':
                rez_lst.append(i_lst)
                break
            # фраза найдена
            # проверим букву перед фразой
            if i > 0:
                if in_lst[i_lst][i - 1].isalpha():  #не повезло - буква
                    continue
            # проверим букву после фразы
            if i + ln_sb < ln_str:
                if in_lst[i_lst][i + ln_sb].isalpha():  #не повезло - буква
                    continue
            if i + ln_sb == ln_str and in_str == 'кострома':
                rez_lst.append(i_lst)
                break
            rez_lst.append(i_lst)
            
        
    return rez_lst

def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем список [тип_улицы, название]
        если известный тип не найден - возвращаем пустой список
    '''
    lst_type_street = [
        'улица',
        'проспект',
        'переулок',
        'бульвар',
        'шоссе',
        'аллея',
        'тупик',
        'проезд',
        'набережная',
        'площадь',
    ]
    out_cort = []
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in lst_type_street:
            if sub.find(ts) >= 0:
                rez = True
                out_cort.append(ts)
                out_cort.append(sub.replace(ts, '').strip())
                break
        if rez: break
    return out_cort

def ordering_house(in_house: str):  # Преобразование строки дом
    '''
        Варианты домов
        1 просто цифра          14
        2 цифра с буквой        30А
        3 цифра / цифра         31/41
        4 цифра буквы цифра     30 корп 3       (корп) вычленяем по "к"
        5 цифра буквы буква(ы)  12 лит А(АД)    вычленяем по "л"
        
        На входе строка с номером дома
        Заменяем двойные пробелы на одинарные и преобразуем в нижний регистр
        
        
        На выходе кортеж (N, str_num) где N первая цифра дома,
        а str_num преобразованный полный номер
        Если ошибка парсинга - ('', 'тип ошибки')
        
    '''
    in_house = in_house.strip()
    if len(in_house) == 0: return ('', 'Не задан номер')
    if in_house.isdigit(): return (in_house, in_house)
    if len(in_house) < 2 and in_house[0].isalpha(): return ('', 'Номер из одной буквы')  # Номер дома не может быть из одной буквы
    # Проходим по строке и если цифры сливаются с буквами вставляем пробел
    n_house = ''
    lst_house = [in_house[0],]
    is_dig = False
    if in_house[0].isdigit(): is_dig = True
    for i in range(1, len(in_house)):
        if in_house[i].isdigit() and is_dig == False:
            is_dig = True
            lst_house.append(' ')
        if in_house[i].isalpha() and is_dig == True:
            is_dig = False
            lst_house.append(' ')
        lst_house.append(in_house[i])
    in_house = ''.join(lst_house)
    # Заменяем двойные пробелы на одинарные
    while '  ' in in_house:
        in_house = in_house.replace('  ', ' ')
    # Проверка на дробь
    lst_house = in_house.split('/')
    if len(lst_house) > 2: return ('', 'Много слешей')
    if len(lst_house) == 2: return (lst_house[0], in_house)
    # Остались корп, лит, буква
    lst_house = in_house.split(' ')
    if len(lst_house) > 3: return ('', 'В номере много позиций')
    if len(lst_house) == 2:  # значит буква - склеиваем как 30А
        lst_house[1] = lst_house[1].upper()
        return (lst_house[0], ''.join(lst_house))
    # анализируем  корп, литер
    if lst_house[1].find('к') >= 0:
        lst_house[1] = ' к'
        return (lst_house[0], ''.join(lst_house))
    if lst_house[1].find('л') >= 0:
        lst_house[1] = ' лит'
        return (lst_house[0], ''.join(lst_house))
    
    return ('', 'Номер не распознан')

def get_txv(data):
    driver = None
    try:
        base_url = 'https://urmdf.ssl.mts.ru'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'phone')
        if len(els) != 1: raise Exception('Ошибка нет поля логин')
        login = data.get('login')
        try:
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка ввода логин')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        password = data.get('password')
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
        # Ищем блок для ввода адреса
        els = driver.find_elements(By.XPATH, '//textarea[@data-testid="search"]')
        if len(els) != 1: raise Exception('Ошибка нет строки ввода адреса')

        # Готовим адресную строку
        region = data.get('region')
        if region == None: region = ''
        city = data.get('city')
        if city == None: raise Exception('Ошибка не заполнено поле город')
        street = data.get('street')
        if street == None: raise Exception('Ошибка не заполнено поле улица')
        house = data.get('house')
        if house == None: raise Exception('Ошибка не заполнено поле дом')
        # С дробями дома не проходят - откидываем дробь
        house = house.split('/')[0]
        apartment = data.get('apartment')
        if apartment == None: apartment = ''
        else: apartment = f' кв. {apartment}'
        address = f'{region} {city} {street} д. {house}{apartment}'
        # Вводим адрес
        try: els[0].send_keys(address)
        except: raise Exception('Ошибка ввода адрес')
        
        # Возможны 3 варианта ответа
        # 1 нет ТхВ блок <div id="results"> .... Нет технической возможности! Проверьте введенный адрес.</div>
        # 2 Множественный выбор блок <div data-testid="suggestions" ....>
        # 3 Есть возможность блок <div id="results"> с перечнем возможностей
        
        driver.implicitly_wait(1)
        while 1:
            time.sleep(5)
            
            els = driver.find_elements(By.XPATH, '//div[@id="results"]')
            if len(els) == 1:
                els_addr = driver.find_elements(By.XPATH, '//textarea[contains(@class, "SearchInput_textArea")]')
                if els_addr[0]: data['pv_address'] = els_addr[0].text
                lst_txt = els[0].text.split('\n')
                lst_txt = [t.strip() for t in lst_txt if len(t.strip()) >= 8]
                data['available_connect'] = '\n'.join(lst_txt)
                break
            
            # Возможно множественный выбор
            els_m = driver.find_elements(By.XPATH, '//div[@data-testid="suggestions"]')
            if len(els_m) == 1:
                els_btn = els_m[0].find_elements(By.TAG_NAME, 'button')
                if len(els_btn) == 0: raise Exception(f'Ошибка нет вариантов выбора адреса: {address}')
                f_lst = []
                for el_btn in els_btn:
                    f_lst.append(el_btn.text)
                i_fnd = find_short(f_lst)
                try: driver.execute_script("arguments[0].click();", els_btn[i_fnd])
                except: raise Exception('Ошибка клика выбора адреса')
                continue
            
            raise Exception(f'Ошибка не распознан адрес: {address}')
        
        if data['available_connect'].find('Нет технической возможности') < 0:
            driver.implicitly_wait(10)
            # Ищем кнопочку перехода
            els = driver.find_elements(By.XPATH, '//button[contains(@class, "SearchInput_Search__SubmitBtn")]')
            if len(els) == 0: raise Exception('Ошибка после адреса нет кнопки активации перехода')
            attr = els[0].get_attribute('disabled')
            if attr != None: raise Exception('')  # Кнопка не активна - выходим
            
            try: driver.execute_script("arguments[0].click();", els[0])
            except: raise Exception('Ошибка клика кнопки активации перехода')
            time.sleep(5)
            ###################### Страница тарифных предложений ######################
            els_section = driver.find_elements(By.XPATH, '//section[contains(@class, "OrderOffers_container")]')
            lst_tar = []
            for el_section in els_section:
                els_art = el_section.find_elements(By.TAG_NAME, 'article')
                for el_art in els_art:
                    els_n = el_art.find_elements(By.TAG_NAME, 'h4')
                    if len(els_n) > 0: lst_tar.append(els_n[0].text)
                    
            data['tarifs_all'] = '\n'.join(lst_tar)
        
        
        # #===========
        # time.sleep(10)
        # with open('out_file.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========



        # time.sleep(3)
        
    except Exception as e:
        return str(e)[:100], data
    finally:
        if driver: driver.quit()
   
    return '', data

def set_txv_to_dj_domconnect(pv_code):
    url = url_host + 'api/set_txv'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'pv_code': pv_code,
        'login': 'GRYURYEV',
        'password': 'UcoTWY',
        'id_lid': '1163386',
        
        'region': 'Калужская область',         # область или город областного значения
        'city': 'Калуга',           # город
        'street': 'улица Ленина',         # улица
        'house': '31',          # дом
        'apartment': '2',          # квартира

    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        pass
        print('Error: requests.get')

def get_txv_in_dj_domconnect(pv_code):
    url = url_host + 'api/get_txv'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'pv_code': pv_code,
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        return 1, []
    if responce.status_code == 200:
        bid_list = json.loads(responce.text)
        return 0, bid_list
    return 2, []

def set_txv_status(status, data):
    url = url_host + 'api/set_txv_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    send_data = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
        'available_connect': data.get('available_connect'),  # Возможность подключения
        'tarifs_all': data.get('tarifs_all'), # список названий тарифных планов
        'pv_address': data.get('pv_address'),
        'status': status,
    }
    bot_log = data.get('bot_log')
    if bot_log:
        send_data['bot_log'] = bot_log
    try:
        responce = requests.post(url, headers=headers, json=send_data)
        st_code = responce.status_code
        if st_code != 200: return st_code
    except Exception as e:
        return str(e)

def send_crm_txv(txv_dict, opsos):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    restrictions = ''
    error_message = txv_dict.get('bot_log')
    if error_message: restrictions += f'{error_message}\n'
    
    pv_address = txv_dict.get('pv_address')
    if pv_address: restrictions += f'{opsos} определил адрес как: {pv_address}\n'
    
    available_connect = txv_dict.get('available_connect')
    if available_connect: restrictions += f'Возможность подключения: {available_connect}\n'
    
    # Проверим статус лида
    upgrade_status = False
    if available_connect.find('Возможность подключения') >= 0:
        url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.get'
        params = {
            'id': txv_dict.get('id_lid'),
        }
        try:
            responce = requests.post(url, headers=headers, params=params)
            st_code = responce.status_code
            if st_code != 200: return st_code, ''
            lid = json.loads(responce.text)
            result = lid.get('result')
            status = result.get('STATUS_ID')
            if status and status == '77': upgrade_status = True
        except Exception as e:
            return str(e), ''

    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }
    up_status = ''
    if upgrade_status:
        params['fields[STATUS_ID]'] = '72'
        up_status = 'Статус обновлен.'

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code, ''
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e), ''
    return '', up_status
    
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

def run_txv_mts(tlg_chat, tlg_token):
    tlg_mess = ''
    
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    if rez:
        tlg_mess = 'Ошибка при загрузке запросов из domconnect.ru'
        r = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(txv_list) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {opsos}: Запросов ТхВ нет')
        return

    # Перелистываем список словарей с заявками
    for txv_dict in txv_list:
        rez, data = get_txv(txv_dict)
        data['bot_log'] = rez
        e, up_status = send_crm_txv(data, opsos)  # ответ в CRM
        crm_mess = f'Ошибка при отправке в СРМ: {e}\n'
        if e:
            tlg_mess += crm_mess
            data['bot_log'] += crm_mess
        address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
        tlg_mess += f'{opsos}: - Выполнен запрос ТхВ\n'
        tlg_mess += f'Адрес: {address}\n'
        djdc = ''
        if rez == '':  # заявка успешно создана
            djdc = set_txv_status(3, data)
            tlg_mess += f'Успешно. {up_status}\n'
        else:  # не прошло
            djdc = set_txv_status(2, data)
            tlg_mess += f'{data.get("bot_log")}\n'
        if djdc: tlg_mess += f'Ошибка при отправке в dj_domconnect: {djdc}'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    start_time = datetime.now()
    
    # url: https://urmdf.ssl.mts.ru
    # login: GRYURYEV
    # password: UcoTWY

    # run_bid_mts()
    
    # txv_dict = {
        # 'pv_code': pv_code,
        # 'login': 'GRYURYEV',
        # 'password': 'UcoTWY',
        # 'id_lid': '1215557',
        
        # # 'region': 'Калужская область',         # область или город областного значения
        # # 'city': 'Калуга',           # город
        # # 'street': 'улица Ленина',         # улица
        # # 'house': '31',          # дом
        # # 'apartment': '2',          # квартира
        
        # # 'region': 'Владимирская область',         # область или город областного значения
        # # 'city': 'Владимир',           # город
        # # 'street': 'ул Фейгина',         # улица
        # # 'house': '10',          # дом
        # # 'apartment': '2',          # квартира
        
        # # # 'region': 'Татарстан',         # область или город областного значения
        # # 'city': 'Казань',           # город
        # # 'street': 'ул Дружинная',         # улица
        # # 'house': '7',          # дом
        # # 'apartment': '2',          # квартира
        
        # # 'region': 'Ярославская область',         # область или город областного значения
        # # 'city': 'Ярославль',           # город
        # # 'street': 'улица Звездная',         # улица
        # # 'house': '31/41',          # дом
        # # 'apartment': '61',          # квартира

        # # 'region': 'Нижегородская область',         # область или город областного значения
        # # 'city': 'Нижний Новгород',           # город
        # # 'street': 'Камчатский пер',         # улица
        # # 'house': '9',          # дом
        # # 'apartment': '10',          # квартира

        # # 'city': 'Реутов',           # город
        # # 'street': 'Носовихинское шоссе',         # улица
        # # 'house': '25',          # дом
        # # # 'apartment': '2',          # квартира
        
        # # 'city': 'Смоленск',           # город
        # # 'street': 'пр-кт Гагарина',         # улица
        # # 'house': '14/2',          # дом
        
        # # 'city': 'Ярославль',           # город
        # # 'street': 'ул Ньютона',         # улица
        # # 'house': '40',          # дом
        # # # 'apartment': '2',          # квартира
        
        # # 'region': 'Смоленская область',         # область или город областного значения
        # # 'city': 'Вязьма',           # город
        # # 'street': 'Кронштадтская улица',         # улица
        # # 'house': '111',          # дом
        # # 'apartment': '10',          # квартира
        
        # 'region': 'Архангельская область',         # область или город областного значения
        # 'city': 'Северодвинск',           # город
        # 'street': 'Лебедева',         # улица
        # 'house': '7',          # дом
        # 'apartment': '10',          # квартира
        
        
        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    
    
    # e, data = get_txv(txv_dict)
    # if e: print(e)
    # print('available_connect:\n', data['available_connect'])
    # print('tarifs_all:\n', data['tarifs_all'])
    # print('pv_address:\n', data['pv_address'])
    
    
    # set_txv_to_dj_domconnect(pv_code)
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for txv_dict in txv_list:
        # for k, v in txv_dict.items():
            # print(k, v)
    # data = {'id': 1, 'pv_address': '55632145', 'bot_log': 'Заявка принята МТС'}
    # r = set_txv_status(0, data)
    # print(r)

    # г Нижний Новгород, Камчатский пер, д 9
    # г Владимир, ул Фейгина, д 10
    # г Казань, ул Дружинная, д 7
    # Реутов, Носовихинское шоссе 25
    # г Смоленск, пр-кт Гагарина, д 14/2
    # г Ярославль, ул Ньютона, д 40
    # г Рязань, ул Черновицкая, д 32
    # г Калининград, ул Пионерская, д 1
    

    
    
    pass
    
    end_time = datetime.now()
    time_str = '\nDuration: {}'.format(end_time - start_time)
    print(time_str)
    # limit_request_line

