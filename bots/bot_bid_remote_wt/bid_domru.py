import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager


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
    
def ordering_street(in_street: str):  # Преобразование строки улица
    '''
        разбиваем строку по запятым, и каждый фрагмент проверяем на
        изветсный тип улицы
        выдаем название без типа улицы
        если известный тип не найден - возвращаем пустую строку
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
    out_street = ''
    lst = in_street.split(',')
    for sub in lst:
        rez = False
        for ts in lst_type_street:
            if sub.find(ts) >= 0:
                rez = True
                out_street = sub.replace(ts, '').strip()
                break
        if rez: break
    return out_street

def set_bid(data):
    driver = None
    try:
        base_url = 'https://internet-tv-dom.ru/operator'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)
        # s = Service(ChromeDriverManager().install())
        # driver = webdriver.Chrome(service=s)

        driver.implicitly_wait(1)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Страница ссылок городов ######################
        city = data.get('city')
        els = driver.find_elements(By.XPATH, '//div[@id="b12356"]')
        if len(els) != 1: raise Exception('Ошибка: нет блока городов')
        els_a = els[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception('Ошибка: нет городов')
        f_ok = False
        url_city = ''
        for el_a in els_a:
            if el_a.text == city:
                url_city = el_a.get_attribute('href')
        if url_city == False: raise Exception(f'Ошибка: город \"{city}\" в списке городов не найден')

        driver.get(url_city)
        time.sleep(3)

        ###################### Страница Логин/Пароль ######################
        els = driver.find_elements(By.XPATH, '//input[@name="login$c"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля логин')
        els[0].send_keys(data.get('login'))
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@name="passwd$c"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля пароль')
        els[0].send_keys(data.get('password'))
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@type="submit"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки Войти')
        els[0].click()
        time.sleep(3)
        ###################### Страница Логин/Пароль ######################
        # frame name="topframe"
        # frame name="leftframe"
        # frame name="mainFrame"
        # driver.switch_to_default_content()  # вернуться к родительскому кадру
        driver.switch_to.frame('leftframe')  # Загружаем фрейм
        time.sleep(3)
        f_ok = False
        els_a = driver.find_elements(By.TAG_NAME, 'a')
        for el_a in els_a:
            if el_a.text == 'Создать договор':
                f_ok = True
                el_a.click()
                time.sleep(3)
        if f_ok == False: raise Exception('Ошибка: Нет ссылки Создать договор')
        
        driver.switch_to.default_content()  # Загружаем родительский фрейм
        time.sleep(1)
        driver.switch_to.frame('mainFrame')  # Загружаем фрейм
        time.sleep(3)
        
        # Жмем кнопку Далее
        els = driver.find_elements(By.XPATH, '//input[@id="dalee_id_button"]')
        if len(els) != 1: raise Exception('Ошибка: Нет кнопки Далее')
        els[0].click()
        time.sleep(3)
        ###################### Блок ввода адреса ######################
        els_addr = driver.find_elements(By.XPATH, '//div[@id="adress_content"]')
        if len(els_addr) != 1: raise Exception('Ошибка: Нет блока адреса')
        el_addr = els_addr[0]
        # Вводим улицу
        els = el_addr.find_elements(By.XPATH, './/input[@id="street_name"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля ввода Улица')
        street = data.get('street')
        if street == None: raise Exception('Ошибка: Не задано значение Улица')
        ord_street = ordering_street(street)
        if ord_street == '': ord_street = street
        els[0].send_keys(ord_street)
        time.sleep(3)
        # отлавливаем подсказку
        f_ok = False
        f_str = []
        els_ul = driver.find_elements(By.TAG_NAME, 'ul')
        for el_ul in els_ul:
            str_class = el_ul.get_attribute('class')
            if str_class.find('display: none') >= 0: continue
            els_li = el_ul.find_elements(By.TAG_NAME, 'li')
            if len(els_li) > 0:
                f_ok = True
                for i in range(len(els_li)):
                    a_s = els_li[i].find_elements(By.TAG_NAME, 'a')
                    f_str.append(a_s[0].text)
                i_sh = find_short(f_str)
                els_li[i_sh].click()
                time.sleep(1)
                
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка: Улица: {street} не найдена')
        # Вводим дом
        els = el_addr.find_elements(By.XPATH, './/input[@id="house_id"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля ввода Дом')
        house = data.get('house')
        if house == None: raise Exception('Ошибка: Не задано значение Дом')
        els[0].send_keys(house)
        time.sleep(3)
        # отлавливаем подсказку
        f_ok = False
        f_str = []
        els_ul = driver.find_elements(By.TAG_NAME, 'ul')
        for el_ul in els_ul:
            str_class = el_ul.get_attribute('class')
            if str_class.find('display: none') >= 0: continue
            els_li = el_ul.find_elements(By.TAG_NAME, 'li')
            if len(els_li) > 0:
                f_ok = True
                for i in range(len(els_li)):
                    a_s = els_li[i].find_elements(By.TAG_NAME, 'a')
                    f_str.append(a_s[0].text)
                i_sh = find_short(f_str)
                els_li[i_sh].click()
                time.sleep(1)
                
            if f_ok == True: break
        if f_ok == False: raise Exception(f'Ошибка: Дом: {house} не найден')
        # Вводим квартиру
        els = el_addr.find_elements(By.XPATH, './/input[@id="anum"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля ввода Квартира')
        apartment = data.get('apartment')
        if apartment == None: raise Exception('Ошибка: Не задано значение Квартира')
        els[0].send_keys(apartment)
        time.sleep(3)
        els = el_addr.find_elements(By.XPATH, './/textarea[@id="adress_comment"]')
        if len(els) != 1: raise Exception('Ошибка: Нет поля комментарий к адресу')
        els[0].click()
        time.sleep(3)
        # Смотрим блок технической возможности
        els = el_addr.find_elements(By.XPATH, './/tr[@id="tr_anum"]')
        if len(els) != 1: raise Exception('Ошибка: Нет блока ТхВ')
        els_td = els[0].find_elements(By.TAG_NAME, 'td')
        if len(els_td) != 3: raise Exception('Ошибка: Неправильная структура блока ТхВ')
        els_div = els_td[2].find_elements(By.TAG_NAME, 'div')
        thv = ''
        for el_div in els_div:
            thv += el_div.text + '\n'
        # Квартира подключена к интернет
        # Квартира подключена к ТВ
        # Квартира подключена к IPTV
        # Квартира не подключена к Домофонии
        # Квартира подключена к видеоконтролю
        # Промо-период доступен
        # print(thv)
        # Жмем кнопку Далее
        els = el_addr.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка: После адреса нет кнопки Далее')
        els[0].click()
        time.sleep(3)
        ###################### Блок операции с договором ######################
        els_dog = driver.find_elements(By.XPATH, '//div[@id="operation_agreement_content"]')
        if len(els_dog) != 1: raise Exception('Ошибка: Нет блока операции с договором')
        el_dog = els_dog[0]
        # Выбираем создать новый договор
        els_sel = el_dog.find_elements(By.XPATH, './/select[@id="sel_agreement"]')
        if len(els_sel) != 1: raise Exception('Ошибка: Нет списка операции с договором')
        els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
        f_ok = False
        for el_opt in els_opt:
            if el_opt.text == 'Создать новый договор':
                f_ok = True
                el_opt.click()
                time.sleep(0.5)
        if f_ok == False: raise Exception('Ошибка: пункт: Создать новый договор не найден')
        # Жмем кнопку Далее
        els = el_dog.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка: После адреса нет кнопки Далее')
        els[0].click()
        time.sleep(3)
        ###################### Блок информация о клиенте ######################
        els_clnt = driver.find_elements(By.XPATH, '//div[@id="client_info_content"]')
        if len(els_clnt) != 1: raise Exception('Ошибка: Нет блока информация о клиенте')
        el_clnt = els_clnt[0]
        # Вводим ФИО
        firstname = data.get('firstname', '')
        patronymic = data.get('patronymic', '')
        lastname = data.get('lastname', '')
        fio = f'{firstname} {patronymic} {lastname}'
        fio = fio.strip()
        if fio == '' or len(fio) < 7: fio = 'Клиент Клиентович'
        els_fio = el_clnt.find_elements(By.XPATH, '//input[@id="client_fio"]')
        if len(els_fio) != 1: raise Exception('Ошибка: Нет поля ввода ФИО клиента')
        els_fio[0].send_keys(fio)
        time.sleep(1)
        # Вводим телефон
        els_tlf = el_clnt.find_elements(By.XPATH, '//input[@id="phone_mobile"]')
        if len(els_tlf) != 1: raise Exception('Ошибка: Нет поля ввода телефона')
        phone = data.get('phone')
        if not phone: raise Exception('Ошибка: Не задано значение телефон')
        els_tlf[0].click()
        time.sleep(0.5)
        els_tlf[0].send_keys(phone[2:])
        time.sleep(1)
        # Жмем кнопку Далее
        els = el_clnt.find_elements(By.XPATH, './/input[@value="Далее"]')
        if len(els) != 1: raise Exception('Ошибка: После Блок информация о клиенте нет кнопки Далее')
        els[0].click()
        time.sleep(3)
        ###################### Блок пакетов услуг ######################
        els_pack = driver.find_elements(By.XPATH, '//table[@id="products"]')
        if len(els_pack) != 1: raise Exception('Ошибка: Нет блока пакетов услуг')
        els_div_pack = els_pack[0].find_elements(By.XPATH, './/div[@class="tarif_pack"]')
        lst_tar = []
        lst_lbl = []
        for el_div_pack in els_div_pack:
            els_lbl = el_div_pack.find_elements(By.TAG_NAME, 'label')
            if els_lbl[0]:
                lst_lbl.append(els_lbl[0])
                lst_tar.append(els_lbl[0].text)
        tarif = data.get('tarif')
        if not tarif: raise Exception('Ошибка: Не задано значение тариф')
        i_fnd = find_string_to_substrs(lst_tar, tarif)
        if i_fnd < 0: raise Exception(f'Ошибка: тариф с фразой(фразами) \"{tarif}\" не найден')
        els_radio = lst_lbl[i_fnd].find_elements(By.TAG_NAME, 'input')
        if len(els_radio) != 1: raise Exception('Ошибка: не найден чекбокс тарифа')
        els_radio[0].click()
        time.sleep(1)
        ###################### Выбор оборудования интернет ######################
        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        router = data.get('router')
        if router == None or router == '':  # если свой роутер
            els_own = driver.find_elements(By.XPATH, '//input[@id="own_router"]')
            if len(els_own) != 1: raise Exception('Ошибка: Нет флажка "свой роутер"')
            els_own[0].click()
            time.sleep(1)
        else:
            lst_intern = router.split('/')
            if len(lst_intern) != 2: raise Exception('Ошибка: поле router должно быть в формате: Название роутера / способ приобретения')
            # Список оборудования для интернет
            lst_ob = []
            els_sel = driver.find_elements(By.XPATH, '//select[@id="select_material_int"]')
            if len(els_sel) != 1: raise Exception('Ошибка: Нет списока оборудования для интернет')
            els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
            for el_opt in els_opt:
                lst_ob.append(el_opt.text)
                # print(el_opt.text)
            i_fnd = find_string_to_substrs(lst_ob, lst_intern[0].strip())
            if i_fnd < 0: raise Exception(f'Ошибка: роутер с фразой(фразами) \"{lst_intern[0].strip()}\" не найден')
            els_opt[i_fnd].click()
            time.sleep(1)
            # Способы приобретения
            lst_ob = []
            els_sel = driver.find_elements(By.XPATH, '//select[@id="select_equip_int"]')
            if len(els_sel) != 1: raise Exception('Ошибка: Нет списока способов приобретения оборудования для интернет')
            els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
            for el_opt in els_opt:
                lst_ob.append(el_opt.text)
            i_fnd = find_string_to_substrs(lst_ob, lst_intern[1].strip())
            if i_fnd < 0: raise Exception(f'Ошибка: роутер с фразой(фразами) \"{lst_intern[1].strip()}\" не найден')
            els_opt[i_fnd].click()
            time.sleep(1)
        ###################### Выбор оборудования ТВ ######################
        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        adapter = data.get('adapter')
        if adapter != None and len(adapter) > 1:  # если указан адаптер ТВ
            lst_adapter = adapter.split('/')
            if len(lst_adapter) != 2: raise Exception('Ошибка: поле adapter должно быть в формате: Название приставки / способ приобретения')
            # Список оборудования для ТВ
            lst_ob = []
            els_sel = driver.find_elements(By.XPATH, '//select[@id="select_material_domru_tv"]')
            if len(els_sel) != 1: raise Exception('Ошибка: Нет списока оборудования для ТВ')
            els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
            for el_opt in els_opt:
                lst_ob.append(el_opt.text)
                # print(el_opt.text)
            i_fnd = find_string_to_substrs(lst_ob, lst_adapter[0].strip())
            if i_fnd < 0: raise Exception(f'Ошибка: адаптер ТВ с фразой(фразами) \"{lst_adapter[0].strip()}\" не найден')
            els_opt[i_fnd].click()
            time.sleep(1)
            # Способы приобретения
            lst_ob = []
            els_sel = driver.find_elements(By.XPATH, '//select[@id="select_equip_domru_tv"]')
            if len(els_sel) != 1: raise Exception('Ошибка: Нет списока способов приобретения оборудования для ТВ')
            els_opt = els_sel[0].find_elements(By.TAG_NAME, 'option')
            for el_opt in els_opt:
                lst_ob.append(el_opt.text)
            i_fnd = find_string_to_substrs(lst_ob, lst_adapter[1].strip())
            if i_fnd < 0: raise Exception(f'Ошибка: адаптер ТВ с фразой(фразами) \"{lst_adapter[1].strip()}\" не найден')
            els_opt[i_fnd].click()
            time.sleep(1)
        # Вводим доп. информацию
        comment = f'Клиент: {data["lastname"]} {data["firstname"]} {data["patronymic"]}\n'
        comment += f'Адрес: {data["city"]}, {data["street"]} д.{data["house"]} кв.{data["apartment"]}\n'
        comment += f'Телефон: {data["phone"]}\n'
        comment += f'Тариф: {data["tarif"]}\n'
        if router: comment += f'Оборудование интернет: {data["router"]}\n'
        if adapter: comment += f'Оборудование TV: {data["adapter"]}\n'
        comment += f'{data["comment"]}\n'
        els = driver.find_elements(By.XPATH, '//textarea[@id="request_info"]')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода комментария')
        els[0].send_keys(comment)
        time.sleep(1)
        # Старица возможно удлиннилась/сдвинулась, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        # Жмем кнопку Далее
        els = driver.find_elements(By.XPATH, '//input[@class="next new_agreement_check"]')
        if len(els) != 1: raise Exception('Ошибка: После Блок тариф и оборудование нет кнопки Далее')
        els[0].click()
        time.sleep(3)
        ###################### Кнопка создать договор ######################
        els = driver.find_elements(By.XPATH, '//input[@id="create"]')
        if len(els) != 1: raise Exception('Ошибка: нет кнопки создать договор')
        els[0].click()
        time.sleep(10)
        # документ pdf отображается, но в коде он как свернутый, закрывать не требуется
        # Ищем номер договора
        els = driver.find_elements(By.XPATH, '//div[@id="new_agree_confirm"]')
        if len(els) != 1: raise Exception('Ошибка: нет блока договора')
        lst_body = els[0].text.split('\n')
        marker = 'Будет создан договор №'
        l_mark = len(marker)
        f_ok = False
        for row in lst_body:
            if row.find(marker) >= 0:
                f_ok = True
                data['bid_number'] = row[l_mark:].strip()
            
        if f_ok == False: raise Exception('Ошибка: номер заявки в ответе не распознан')
        print(f'Создана заявка {data["bid_number"]}')

        # Жмем кнопку Продолжить
        els = driver.find_elements(By.XPATH, '//input[@value="Продолжить"]')
        if len(els) != 1: raise Exception('Ошибка: После создания договора нет кнопки Продолжить')
        # Обычным способом чекбокс не отмечается - element not interactable
        driver.execute_script("arguments[0].click();", els[0])
        time.sleep(3)
            
        
        
        # time.sleep(5)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # driver.quit()
        # return '', data
        
        
    except Exception as e:
        print(e)
        return e, data,
    finally: driver.quit()   
    
    return '', data, 

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_domru'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'login': 'sinitsin',
        'password': 'BVNocturne20',
        'id_lid': '1188357',
        
        'city': 'Ярославль',           # город
        # 'street': 'улица Пирогова',         # улица
        'street': 'улица Индустриальн',         # улица
        'house': '21',          # дом
        'apartment': '2',          # квартира
        
        # В названиях тарифных планов, названиях роутеров, приставок и способов приобретения
        # может быть указано либо название целиком либо набор ключевых фраз через точку с запятой
        'tarif': 'Засмотрись ; 250', # Название тарифного плана
        # router = (Название роутера / способ приобретения) - заполняем если нужен роутер
        'router': 'Система Wi-Fi ; Mesh Tenda / Рассрочка ; 12 мес ',
        # 'router': '',
        # adapter = (Название TV приставки / способ приобретения) - заполняем если нужено оборудование TV
        # 'adapter': 'телевизионная приставка ; Movix/ Рассрочка', 
        'adapter': '', 
        
        'firstname': 'Иван',
        'patronymic': 'Иванович',
        'lastname': '',
        'phone': '79011111113',
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
    url = url_host + 'api/get_bid_domru'
    
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
    url = url_host + 'api/set_bid_domru_status'
    
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
        'fields[UF_CRM_1493413514]': 1,
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
    # https://crm.domconnect.ru/crm/lead/details/1188357/

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

def run_bid_domru(tlg_chat, tlg_token):
    opsos = 'ДомРу'
    
    rez, bid_list = get_did_in_dj_domconnect()
    if rez:
        tlg_mess = 'Ошибка при загрузке заявок из domconnect.ru'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print('TelegramMessage:', r)
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
            address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}\n'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Логин: {data.get("partner_login")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'Ошибка: {data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    # https://internet-tv-dom.ru/operator
    # login: sinitsin
    # password: BVNocturne20

    # # личный бот @infra
    # TELEGRAM_CHAT_ID = '1740645090'
    # TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    # run_bid_domru(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    # bid_dict = {
        # 'login': 'sinitsin',
        # 'password': 'BVNocturne20',
        # 'id_lid': '1163386',
        
        # # 'region': 'Калужская область',         # область или город областного значения
        # 'city': 'Ярославль',           # город
        # # 'street': 'улица Пирогова',         # улица
        # 'street': 'улица Индустриальн',         # улица
        # 'house': '21',          # дом
        # 'apartment': '2',          # квартира
        
        # # В названиях тарифных планов, названиях роутеров, приставок и способов приобретения
        # # может быть указано либо название целиком либо набор ключевых фраз через точку с запятой
        # 'tarif': 'Засмотрись ; 250', # Название тарифного плана
        # # router = (Название роутера / способ приобретения) - заполняем если нужен роутер
        # 'router': 'Система Wi-Fi ; Mesh Tenda / Рассрочка ; 12 мес ',
        # # 'router': '',
        # # adapter = (Название TV приставки / способ приобретения) - заполняем если нужено оборудование TV
        # 'adapter': 'телевизионная приставка ; Movix/ Рассрочка', 
        # # 'adapter': '', 
        
        
        # 'firstname': 'Иван',
        # 'patronymic': '',
        # 'lastname': '',
        # 'phone': '79011111113',
        # 'comment': 'Тестовая заявка, просьба не обрабатывать',          # коментарий обязательно: подъезд этаж
        # 'bid_number': '',          # номер заявки
    # }
    
    
    # e, data = set_bid(bid_dict)
    
    
    # # print(data['bid_number'])
    
    # set_did_to_dj_domconnect()
    # rez, bid_list = get_did_in_dj_domconnect()
    # for bid_dict in bid_list:
        # for k, v in bid_dict.items():
            # print(k, v)
    # data = {'id': 1, 'bid_number': '55632145', 'bot_log': 'Заявка принята'}
    # set_bid_status(3, data)
    
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



    
    pass
