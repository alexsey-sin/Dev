import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re

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

def find_short_tup(f_lst):
    '''
        На входе список кортежей.
        в кортеже индкс фразы на странице и фраза
        Поиск самой короткой фразы в списке и выдача её индекса на странице
    '''
    l_min = 10000
    i_min = 0
    for i in range(len(f_lst)):
        l_phr = len(f_lst[i][1])
        if l_phr < l_min:
            l_min = l_phr
            i_min = i
    i_out = f_lst[i_min][0]
    return i_out
    
def set_bid(data):
    driver = None
    rez_set_bid = ''
    try:
        base_url = 'https://partnerweb.beeline.ru/'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(2)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'id_login')
        if els[0]:
            try: els[0].send_keys(data['partner_login'])
            except: raise Exception('Ошибка ввода 1')
        else: raise Exception('Ошибка авторизация')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'id_workercode')
        if els[0]:
            try: els[0].send_keys(data['partner_workercode'])
            except: raise Exception('Ошибка ввода 2')
        else: raise Exception('Ошибка авторизации')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'id_password')
        if els[0]:
            try: els[0].send_keys(data['partner_password'])
            except: raise Exception('Ошибка ввода 3')
        else: raise Exception('Ошибка авторизация')
        time.sleep(1)
        
        els = driver.find_elements(By.TAG_NAME, 'button')
        if els[0]:
            try: els[0].click()
            except: raise Exception('Ошибка клика 1')
        else: raise Exception('Ошибка авторизация')
        time.sleep(3)
        ###################### Главная страница ######################
        
        els_a = driver.find_elements(By.TAG_NAME, 'a')
        el = None
        for el_a in els_a:
            link = el_a.get_attribute('href')
            if link and link.find('/ngapp#!/checkaddress/search') >= 0:
                el = el_a
                break
        if el:
            try: el.click()
            except: raise Exception('Ошибка клика 2')
        else: raise Exception('Ошибка переход к списку городов')
        time.sleep(3)
        ###################### Страница поиска адреса ######################
        # Вводим название населенного пункта
        els = driver.find_elements(By.ID, 'btn-append-to-body')
        if len(els) != 1: raise Exception('Ошибка нет поля ввод города')
        city = data.get('city')
        if city:
            try: els[0].send_keys(city)
            except: raise Exception('Ошибка ввода 4')
        else: raise Exception('Ошибка не задан город')
        time.sleep(3)
        # Ищем всплывающее контекстное меню с подсказкой города
        driver.implicitly_wait(1)

        els_ul = driver.find_elements(By.XPATH, '//ul[@class="dropdown-menu ng-scope"]')
        if len(els_ul) != 1: raise Exception('Ошибка нет всплывающее контекстное меню с подсказкой города')
        els_a = els_ul[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception(f'Ошибка Населенный пункт {city} не найден')
        elif len(els_a) == 1:
            try: els_a[0].click()
            except: raise Exception('Ошибка клика 3')
        else:
            # Здесь можно для каждого нас. пункта прописать отдельные правила
            # по выбору пункта всплывающего меню
            if city == 'Ярославль':
                try: els_a[0].click()
                except: raise Exception('Ошибка клика 4')
            elif city == 'Кострома':
                try: els_a[0].click()
                except: raise Exception('Ошибка клика 5')
            else:
                # Множественный выбор
                lst_nas_punkt = []
                for el in els_a:
                    lst_nas_punkt.append(el.text)
                lst_cheq = check_equality_citys(lst_nas_punkt, city)
                if len(lst_cheq) == 0: raise Exception(f'Ошибка Населенный пункт: {city} не найден2')
                elif len(lst_cheq) > 1:
                    lst_tup = []
                    for ci in lst_cheq:
                        lst_tup.append((ci, lst_nas_punkt[ci]))
                    i_tup = find_short_tup(lst_tup)
                    try: els_a[i_tup].click()
                    except: raise Exception('Ошибка клика 6')
        
        time.sleep(3)
        
        # Вводим название улицы
        els_street = driver.find_elements(By.XPATH, '//input[@placeholder="Улица"]')
        if len(els_street) != 1: raise Exception('Ошибка не найдено поле ввода названия улицы')
        el_street = els_street[0]
        # Удалим если что-то уже введено
        try: el_street.send_keys(Keys.CONTROL + 'a')
        except: raise Exception('Ошибка ввода 5')
        time.sleep(0.2)
        try: el_street.send_keys(Keys.DELETE)
        except: raise Exception('Ошибка ввода 6')
        time.sleep(0.2)

        # Преобразуем в нормальный вид [тип, название]
        street = data.get('street')
        if not street: raise Exception('Ошибка не задано поле улица')
        street = street.replace('ё', 'е')
        lst_street = ordering_street(street)
        if lst_street:  # если распознали по типу
            try: el_street.send_keys(lst_street[1])
            except: raise Exception('Ошибка ввода 7')
        else:  # если нет - вводим как есть
            try: el_street.send_keys(street)
            except: raise Exception('Ошибка ввода 8')
            lst_street = ('улица', street)
        
        # Нажимаем кнопку найти
        els_button = driver.find_elements(By.XPATH, '//button[@ng-click="checkaddressAbstractController.searchPattern()"]')
        if len(els_button) != 1: raise Exception('Ошибка не найдена кнопка поиск улицы')
        try: els_button[0].click()
        except: raise Exception('Ошибка клика 7')
        time.sleep(5)
        
        driver.implicitly_wait(1)
        # Определим - найдена ли улица однозначно
        els_div = driver.find_elements(By.XPATH, '//div[@ng-hide="checkaddressAbstractController.loading"]')
        if len(els_div) > 0:  # Проблемма - улица не найдена или множественный выбор
            streets = []
            for el_div in els_div:
                if el_div.text == 'Улицы не найдены':
                    raise Exception(f'Ошибка улица {street} не найдена.')
            
            # Ищем всплывающее контекстное меню с подсказкой города
            els_div = driver.find_elements(By.ID, 'listStart')
            if len(els_div) != 1: raise Exception('Ошибка нет всплывающее контекстное меню с подсказкой улицы')
            els_a = els_div[0].find_elements(By.XPATH, './*//a[@class="link ng-binding"]')
            if len(els_a) == 0: raise Exception(f'Ошибка улица {street} не найдена2.')
            f_lst = []
            for i in range(len(els_a)):
                name_street = els_a[i].text
                if name_street.find(lst_street[1]) >= 0 and name_street.find(lst_street[0]) >= 0: f_lst.append((i, name_street))
            
            f_ind = find_short_tup(f_lst)
            try: els_a[f_ind].click()
            except: raise Exception('Ошибка клика 8')
            time.sleep(5)
        
        driver.implicitly_wait(10)
        time.sleep(5)
        # Ищем таблицу с номерами домов
        els_table = driver.find_elements(By.TAG_NAME, 'table')
        if len(els_table) != 1: raise Exception('Ошибка нет таблицы домов')
        el_table = els_table[0]
        
        els_a = el_table.find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception('Ошибка В таблице домов нет элементов')
        
        house = data.get('house')
        if house == None: raise Exception('Ошибка не задан номер дома')
        c_house = ordering_house(house)
        if c_house[0] == '': raise Exception(f'Ошибка не распознан номер дома \"{house}\"')
        el = None
        for el_a in els_a:
            if el_a.text == c_house[1]:
                el = el_a
                break
        
        if el:
            try: el.click()
            except: raise Exception('Ошибка клика 9')
        else: raise Exception(f'Ошибка Дом {house} не найден')
        time.sleep(5)
        
        els_b = driver.find_elements(By.TAG_NAME, 'button')
        el = None
        for el_b in els_b:
            link = el_b.get_attribute('ng-click')
            if link and link.find('ok()') >= 0:
                el = el_b
                break
        if el:
            try: el.click()
            except: raise Exception('Ошибка клика 10')
        else: raise Exception('Ошибка нет кнопки продолжить после прочтения ограничений')
        time.sleep(3)
        ###################### Страница ввода заявки ######################
        # Ищем квартиру
        driver.set_window_size(300,800)
        time.sleep(2)
        try:
            el_h = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/abon-form/form/div[1]/div[3]/div[2]/div[2]/div/div/input')
            el_h.send_keys(data['apartment'])
        except:
            raise Exception('Ошибка не могу ввести номер дома')
        time.sleep(1)
        
        # Вводим фамилию
        els_ln = driver.find_elements(By.XPATH, '//input[@name="client_surname"]')
        if len(els_ln) != 1: raise Exception('Ошибка нет поля ввода фамилии')
        try: els_ln[0].send_keys(data['lastname'])
        except: raise Exception('Ошибка ввода 9')
        time.sleep(1)
        # Вводим имя
        els_fn = driver.find_elements(By.XPATH, '//input[@name="client_name"]')
        if len(els_fn) != 1: raise Exception('Ошибка нет поля ввода имени')
        try: els_fn[0].send_keys(data['firstname'])
        except: raise Exception('Ошибка ввода 10')
        time.sleep(1)
        # Вводим отчество
        els_fn = driver.find_elements(By.XPATH, '//input[@name="client_patrony"]')
        if len(els_fn) != 1: raise Exception('Ошибка нет поля ввода отчества')
        try: els_fn[0].send_keys(data['patronymic'])
        except: raise Exception('Ошибка ввода 11')
        time.sleep(1)
        # Вводим телефон
        els_ph = driver.find_elements(By.XPATH, '//input[@name="phone_number_1"]')
        if len(els_ph) != 1: raise Exception('Ошибка нет поля ввода телефона')
        phone = data.get('phone')
        if phone == None: raise Exception('Ошибка не задан телефон')
        try: els_ph[0].send_keys(phone[1:])
        except: raise Exception('Ошибка ввода 12')
        time.sleep(1)
        driver.set_window_size(1000,1000)
        time.sleep(3)
        
        # Определим тип абонента
        type_abonent = data.get('type_abonent')
        if type_abonent == None: raise Exception('Ошибка нет type_abonent')
        
        if str(type_abonent) == '0':
            # Ищем вкладку пакетные предложения
            els_pack = driver.find_elements(By.XPATH, '//div[@ng-click="$servCtrl.stype.tab = 3; $servCtrl.stype.presetsClicked = true;"]')
            if len(els_pack) != 1: raise Exception('Ошибка нет вкладки пакетные предложения')
            try: els_pack[0].click()
            except: raise Exception('Ошибка клика 11')

        time.sleep(10)
        
        # Ищем тарифные предложения
        els_tarifs = driver.find_elements(By.XPATH, '//label[@class="title cur-pointer ng-binding title--normal title--dotted"]')
        tarif = data['tarif']
        lst_new_tarif = []
        # Проверяем наличие цифры
        dig = re.search(r'\d{3,}', tarif)
        if dig: lst_new_tarif.append(dig.group().strip())
        # Проверяем наличие ТВ в тарифном плане
        tv = re.search(r'ТВ', tarif)
        if tv: lst_new_tarif.append(tv.group().strip())
        if lst_new_tarif: tarif = ';'.join(lst_new_tarif)
        
        lst_tarif = []
        for el_tarif in els_tarifs: lst_tarif.append(el_tarif.text.strip())
        f_ind = find_string_to_substrs(lst_tarif, tarif)
        
        if f_ind < 0: raise Exception(f'Ошибка Тариф {tarif} не найден')
        driver.execute_script("arguments[0].scrollIntoView();", els_tarifs[f_ind])
        time.sleep(1)
        try: els_tarifs[f_ind].click()
        except: raise Exception('Ошибка клика 12')
        time.sleep(10)
        
        # Страница возможно сдвинулась и верхняя кнопка не видна, прокрутим страницу вниз
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(1)
        
        dt_grafic = data.get('dt_grafic')
        if dt_grafic:
            # ищем кнопку назначить в график
            els_button = driver.find_elements(By.XPATH, '//button[@ng-click="$newAdrCtrl.createWithSchedule()"]')
            if len(els_button) != 1: raise Exception('Ошибка нет кнопки назначить в график')
            try: els_button[0].click()
            except: raise Exception('Ошибка клика 13')
        else:
            # ищем кнопку отправить без назначения в график
            els_button = driver.find_elements(By.XPATH, '//button[@ng-click="$newAdrCtrl.create()"]')
            if len(els_button) != 1: raise Exception('Ошибка нет кнопки отправить без назначения в график')
            try: els_button[0].click()
            except: raise Exception('Ошибка клика 14')
        time.sleep(10)
            
        # смотрим ответ
        modal_divs = driver.find_elements(By.XPATH, '//div[@uib-modal-window="modal-window"]')
        if len(modal_divs) != 1: raise Exception('Ошибка нет модального окна ответа на заявку')
        els_strong = modal_divs[0].find_elements(By.TAG_NAME, 'strong')
        bid_ok = 0
        answer = ''
        for el_strong in els_strong:
            answer = el_strong.text.strip()
            if answer.isdigit(): data['ctn_abonent'] = answer; bid_ok += 1;
            if answer.find('№') >= 0: data['bid_number'] = answer; bid_ok += 1;
        
        if bid_ok == 0:
            modal_cont = driver.find_elements(By.XPATH, '//div[@class="modal-content"]')
            if len(modal_cont) == 1:
                answer = modal_cont[0].text
                raise Exception(f'Ошибка {answer}')
            else:
                raise Exception('Ошибка не распознан ответ на заявку')
        elif bid_ok == 1:
            raise Exception('Ошибка распознавания ответа на заявку')
        print(f'Создана заявка:\nCTN: {data.get("ctn_abonent")}\nНомер: {data.get("bid_number")}')

        # Нажимаем продолжить для назначения графика
        try:
            if dt_grafic:
                print('Назначаем график', dt_grafic)
                els_button = driver.find_elements(By.XPATH, '//button[@ng-click="close()"]')
                if len(els_button) != 1: raise Exception('Ошибка нет кнопки продолжить')
                try: els_button[0].click()
                except: raise Exception('Ошибка клика 15')
                time.sleep(10)

                # Берем доп информацию
                els = driver.find_elements(By.XPATH, '//div[@class="card__content"]')
                if len(els) != 1: raise Exception('Ошибка нет поля доп.информация.')
                data['grafic_dop_info'] = els[0].text
                print('Dop info:')
                print(data['grafic_dop_info'])
                

                # Кликаем календарь
                els_btn_cld = driver.find_elements(By.XPATH, '//button[@ng-click="showCalendar()"]')
                if len(els_btn_cld) != 1: raise Exception('Ошибка нет кнопки календарь')
                try: els_btn_cld[0].click()
                except: raise Exception('Ошибка клика 16')
                time.sleep(10)
                
                els_cld = driver.find_elements(By.TAG_NAME, 'schedules-calendar')
                if len(els_cld) != 1: raise Exception('Ошибка нет блока календарь')
                
                # Определяем дату
                txt_months = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
                els_month = els_cld[0].find_elements(By.XPATH, './/div[@class="schedules-calendar"]')
                if len(els_month) == 0: raise Exception('Ошибка Календарь не содержит блоки месяцев.')
                dt_gr = dt_grafic.split(' ')
                lst_date = dt_gr[0].split('.')
                if len(lst_date) != 3: raise Exception(f'Ошибка структуры даты {".".join(lst_date)}')
                try: i_mon = int(lst_date[1])
                except: raise Exception('Ошибка числа месяца календаря.')
                if i_mon < 1 or i_mon > 12: raise Exception(f'Ошибка месяц даты {".".join(lst_date)} не корректен')
                s_mon = f'{txt_months[i_mon]} {lst_date[2]}'
                try:
                    free_first_day = ''
                    f_month = False
                    f_day = False
                    for el_month in els_month:
                        f_month = False
                        f_day = False
                        els_tit_month = el_month.find_elements(By.XPATH, './/div[@class="schedules-calendar__caption title title--s title--normal ng-binding"]')
                        if len(els_tit_month) != 1: raise Exception('Ошибка структуры календаря.Титул.')
                        if els_tit_month[0].text.strip().lower() == s_mon: f_month = True
                        els_days = el_month.find_elements(By.XPATH, './/div[@class="schedules-calendar__day schedules-calendar__day--hover-border ng-binding ng-scope schedules-calendar__day--color-yellow"]')
                        for el_days in els_days:
                            if free_first_day == '': free_first_day = f'{el_days.text} {els_tit_month[0].text}'
                            cal_day = el_days.text.strip()
                            if len(cal_day) == 1: cal_day = '0' + cal_day
                            if cal_day == lst_date[0].strip():
                                f_day = True
                                if f_month:
                                    time.sleep(10)
                                    try: el_days.click()
                                    except: raise Exception('Ошибка клика 17')
                                    # print('Day click.')
                                    time.sleep(10)
                    if f_month == False or f_day == False:
                        er_mess = f'Ошибка день \"{lst_date[0]} {s_mon}\" в календаре не найден.'
                        if free_first_day: er_mess += f' Ближайший свободный день: {free_first_day}'
                        raise Exception(er_mess)
                except: pass
                # print('Date is Ok')
                
                # Определяем время
                time.sleep(20)
                els_time = driver.find_elements(By.XPATH, '//span[@class="ui-select-toggle"]')
                if len(els_time) != 1: raise Exception('Ошибка Нет поля выбора время.')
                try: els_time[0].click()
                except: raise Exception('Ошибка клика 18')
                time.sleep(2)
                
                els_li_times = driver.find_elements(By.XPATH, '//li[@id="ui-select-choices-0"]')
                if len(els_li_times) != 1: raise Exception('Ошибка Нет блока время.')
                els_times = els_li_times[0].find_elements(By.XPATH, './/span[@class="ng-binding ng-scope"]')
                if len(els_times) == 0: raise Exception('Ошибка Нет вариантов выбора время.')

                lst_time = dt_gr[1].split('-')
                if len(lst_time) != 2: raise Exception(f'Ошибка структуры времени {"-".join(lst_time)}')

                lst_avl_time = []
                for el_times in els_times: lst_avl_time.append(el_times.text)
                i_time = -1
                for i in range(len(lst_avl_time)):
                    if lst_avl_time[i].find(lst_time[0]) >= 0 and lst_avl_time[i].find(lst_time[1]) >= 0: i_time = i
                        
                if i_time < 0:  # Нужный тайм слот не найден
                    lst_tmp = []
                    try:
                        for l_time in lst_avl_time:
                            ll_time = l_time.split(' — ')
                            t1_t = ll_time[0].split(':')
                            t2_t = ll_time[1].split(':')
                            lst_tmp.append(f'{t1_t[0]}-{t2_t[0]}')
                    except: print('Ошибка сбора списка времени.')
                    e_mess = f'Ошибка период времени {dt_gr[1]} не доступен.'
                    if lst_tmp: e_mess += f'Возможны варианты: {";".join(lst_tmp)}'
                    raise Exception(e_mess)
                time.sleep(3)
                try: els_times[i_time].click()
                except: raise Exception('Ошибка клика 19')
                time.sleep(2)
                # print('time Ok:', i_time)

                # Поля подъезд, этаж, домофон
                els = driver.find_elements(By.XPATH, '//input[@ng-model="schedule.address.entrance"]')
                if len(els) != 1: raise Exception('Ошибка нет поля подъезд.')
                try: els[0].send_keys('-')
                except: raise Exception('Ошибка ввода 13')
                time.sleep(2)
            
                els = driver.find_elements(By.XPATH, '//input[@ng-model="schedule.address.floor"]')
                if len(els) != 1: raise Exception('Ошибка нет поля этаж.')
                try: els[0].send_keys('-')
                except: raise Exception('Ошибка ввода 14')
                time.sleep(2)
            
                els = driver.find_elements(By.XPATH, '//input[@ng-model="schedule.address.code"]')
                if len(els) != 1: raise Exception('Ошибка нет поля домофон.')
                try: els[0].send_keys('-')
                except: raise Exception('Ошибка ввода 15')
                time.sleep(2)
                
                # Кликаем финальную кнопку Назначить в график
                els = driver.find_elements(By.XPATH, '//button[@ng-disabled="isScheduleDisable()"]')
                if len(els) != 1: raise Exception('Ошибка нет кнопки Назначить в график(Финальная).')
                try: els[0].click()
                except: raise Exception('Ошибка клика 20')
                time.sleep(5)
                
                

                
        except Exception as e:
            data['grafic_error'] = str(e)
        
        # #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========
        # raise Exception('Finish')
        
    except Exception as e:
        rez_set_bid = str(e)
    finally:
        # time.sleep(5)
        # with open('out_file.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        driver.quit()
   
    return rez_set_bid, data

def set_did_to_dj_domconnect():
    url = url_host + 'api/set_bid_beeline'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'partner_login': '0K23-181',
        'partner_workercode': '1010000101',
        'partner_password': 'CgslU7tfFsK5w8',
        'id_lid': '1163386',
        'city': 'Ярославль',
        'street': 'улица Труфанова',
        'house': '29 корп 3',
        'apartment': '65',
        'firstname': 'Тест',
        'lastname': 'Тест',
        'patronymic': 'Тест',
        'phone': '79111234567',
        'type_abonent': '0',
        'tarif': 'Интернет 100 Мбит',
        'dt_grafic': '02.12.2021 16-18',
    }# Близкие люди 4 +
    
    try:
        responce = requests.get(url, headers=headers, params=params)
        print(responce.status_code)
        print(responce.text)
    except:
        pass
        print('Error: requests.get')

def get_did_in_dj_domconnect():
    url = url_host + 'api/get_bid_beeline'
    
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
    url = url_host + 'api/set_bid_beeline_status'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    send_data = {
        'key': 'Q8kGM1HfWz',
        'id': data.get('id'),
        'ctn_abonent': data.get('ctn_abonent'),
        'bid_number': data.get('bid_number'),
        'grafic_error': data.get('grafic_error'),
        'grafic_dop_info': data.get('grafic_dop_info'),
        'status': status,
    }
    bot_log = data.get('bot_log')
    if bot_log:
        send_data['bot_log'] = bot_log
    try:
        responce = requests.post(url, headers=headers, json=send_data)
    except Exception as e:
        print('set_bid_status')
        print(str(e))

def send_crm_bid(bid_dict):
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': user_agent_val,
    }

    grafic = bid_dict.get('dt_grafic')
    err_grafic = bid_dict.get('grafic_error')
    txt_grafic = ''
    number_bid_ctn = f'Заявка: {bid_dict.get("bid_number")} / CTN: {bid_dict.get("ctn_abonent")}'
    if grafic:
        if err_grafic:
            txt_grafic = f'Назначение в график: {err_grafic}'
            number_bid_ctn += ' ' + err_grafic
        else:
            txt_grafic = f'Назначено в график: {grafic}'
    partner_web = {
        'F03': '519',
        'S01-181': '3057',
        '0K23-181': '3000',
        'S24-61': '3001',
        'S06': '521',
        '651-37': '520',
    }
    pw = partner_web.get(bid_dict.get("partner_login"))
    params = {
        'id': bid_dict.get('id_lid'),
        'fields[UF_CRM_5864F4DAAC508]': number_bid_ctn,
        'fields[UF_CRM_1493413514]': 'OTHER',
        'fields[UF_CRM_5864F4DA85D5A]': bid_dict.get('tarif'),
        'fields[UF_CRM_1499386906]': pw,  # PartnerWEB
        'fields[UF_CRM_1638258034630]': txt_grafic,
        'fields[UF_CRM_1638258458516]': bid_dict.get('grafic_dop_info'),
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
    except Exception as e:
        print('set_bid_status')
        print(e)
        return 600
    return r.status_code

def run_bid_beeline(tlg_chat, tlg_token):
    opsos = 'Билайн'
    
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
            tlg_mess += f'CTN: {data.get("ctn_abonent")}\n'
            tlg_mess += f'Номер заявки: {data.get("bid_number")}\n'
            grafic = data.get('dt_grafic')
            err_gr = data.get('grafic_error')
            if grafic:
                if err_gr:
                    tlg_mess += f'Назначение в график: {err_gr}\n'
                else:
                    tlg_mess += f'Назначено в график: {grafic}\n'
        else:  # не прошло
            set_bid_status(2, data)
            tlg_mess = f'{opsos}:\n'
            address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
            fio = f'{data.get("firstname")} {data.get("patronymic")} {data.get("lastname")}'
            tlg_mess += f'Лид: {data.get("id_lid")}\n'
            tlg_mess += f'Логин: {data.get("partner_login")}\n'
            tlg_mess += f'Адрес: {address}\n'
            tlg_mess += f'ФИО: {fio}\n'
            tlg_mess += f'{data.get("bot_log")}\n'
        r = send_telegram(tlg_chat, tlg_token, tlg_mess)
        print(tlg_mess)
        print('TelegramMessage:', r)
    #================================================


if __name__ == '__main__':
    # https://partnerweb.beeline.ru
    # set_did_to_dj_domconnect()
    
    # data = {'id': 15, 'grafic_error': 'type error', 'grafic_dop_info': 'uuuu grafic_dop_info'}
    # set_bid_status(2, data)
    
    # rez, bid_list = get_did_in_dj_domconnect()
    # for val in bid_list:
        # print(val)
    
    
    # data = {
        # 'partner_login': 'S01-181',
        # 'partner_workercode': '1999999222',
        # 'partner_password': '8GFysus@kffs7',
        # 'id_lid': '1259587',
        # 'city': 'Москва',
        # 'street': 'Новощукинская улица',
        # 'house': '4',
        # 'apartment': '151',
        # # 'city': 'Иннополис',
        # # 'street': 'Спортивная улица',
        # # 'house': '138',
        # # 'apartment': '91',
        # 'firstname': 'Валерия',
        # 'lastname': '-',
        # 'patronymic': '-',
        # 'phone': '79111234567',
        # 'type_abonent': '0',
        # 'tarif': 'Интернет 100 Мбит с ТВ',
        # # 'tarif': 'Интернет 100 Мбит',
        
        # 'dt_grafic': '',
        # # # 'dt_grafic': '02.12.2021 16-18',
        # # 'grafic_error': '',
        # # 'grafic_dop_info': '',
    # }
    # rez, data = set_bid(data)
    # if rez: print(rez)
    # # gr_e = data['grafic_error']
    # if gr_e:
        # print('gr_e')
        # print(gr_e)
    
    

    
    
    pass
    '''
        1 аккаунт
            S01-181
            1999999222
            8GFysus@kffs7

        2 аккаунт
            0K23-181
            1010000101
            FudlU7tfFsK5g6
    '''