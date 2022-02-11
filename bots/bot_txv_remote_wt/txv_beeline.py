import os
import time
from datetime import datetime
import requests  # pip install requests
import json
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'
opsos = 'Билайн'
pv_code = 1
workercode = '1010000101'


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
    
def get_txv(data):
    driver = None
    try:
        base_url = 'https://partnerweb.beeline.ru/'
        
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(3)
        
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'id_login')
        if len(els) != 1: raise Exception('Ошибка нет поля логин')
        login = data.get('login')
        try: 
            if login: els[0].send_keys(login)
            else: raise Exception('Ошибка не задан логин')
        except: raise Exception('Ошибка действий 01')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'id_workercode')
        if len(els) != 1: raise Exception('Ошибка нет поля workercode')
        try: els[0].send_keys(workercode)
        except: raise Exception('Ошибка действий 02')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'id_password')
        if len(els) != 1: raise Exception('Ошибка нет поля пароль')
        password = data.get('password')
        try:
            if password: els[0].send_keys(password)
            else: raise Exception('Ошибка не задан пароль')
        except: raise Exception('Ошибка действий 03')
        time.sleep(1)

        els = driver.find_elements(By.TAG_NAME, 'button')
        if len(els) != 1: raise Exception('Ошибка нет кнопки войти')
        try: els[0].click()
        except: raise Exception('Ошибка действий 04')
        time.sleep(5)
        ###################### Главная страница ######################
        els_a = driver.find_elements(By.XPATH, '//a[@href="/ngapp#!/checkaddress/search"]')
        if len(els_a) != 1: raise Exception('Ошибка нет ссылки перейти к списку городов')
        try: els_a[0].click()
        except: raise Exception('Ошибка действий 05')
        time.sleep(5)
        ###################### Страница поиска адреса ######################
        # Вводим название населенного пункта
        els = driver.find_elements(By.ID, 'btn-append-to-body')
        if len(els) != 1: raise Exception('Ошибка нет поля ввода города')
        city = data.get('city')
        try:
            if city: els[0].send_keys(city)
            else: raise Exception('Ошибка не задан город')
        except: raise Exception('Ошибка действий 06')
        time.sleep(3)
        
        # Ищем всплывающее контекстное меню с подсказкой города
        driver.implicitly_wait(1)

        els_ul = driver.find_elements(By.XPATH, '//ul[@class="dropdown-menu ng-scope"]')
        if len(els_ul) != 1: raise Exception('Ошибка нет всплывающее контекстное меню с подсказкой города')
        els_a = els_ul[0].find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception(f'Ошибка Населенный пункт {city} не найден')
        elif len(els_a) == 1:
            try: els_a[0].click()
            except: raise Exception('Ошибка действий 07')
        else:
            # Здесь можно для каждого нас. пункта прописать отдельные правила
            # по выбору пункта всплывающего меню
            if city == 'Ярославль':
                try: els_a[0].click()
                except: raise Exception('Ошибка действий 08')
            elif city == 'Кострома':
                try: els_a[0].click()
                except: raise Exception('Ошибка действий 09')
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
                    except: raise Exception('Ошибка действий 10')
        
        time.sleep(3)

        # Вводим название улицы
        els_street = driver.find_elements(By.XPATH, '//input[@placeholder="Улица"]')
        if len(els_street) != 1: raise Exception('Ошибка не найдено поле ввода названия улицы')
        street = data.get('street')
        if street == '': raise Exception('Ошибка не задана улица')
        # Преобразуем в нормальный вид [тип, название]
        lst_street = ordering_street(street)
        if lst_street:  # если распознали по типу
            try: els_street[0].send_keys(lst_street[1])
            except: raise Exception('Ошибка действий 11')
        else:  # если нет - вводим как есть
            try: els_street[0].send_keys(street)
            except: raise Exception('Ошибка действий 12')
        
        # Нажимаем кнопку найти
        els_button = driver.find_elements(By.XPATH, '//button[@ng-click="checkaddressAbstractController.searchPattern()"]')
        if len(els_button) != 1: raise Exception('Ошибка не найдена кнопка поиск улицы')
        try: els_button[0].click()
        except: raise Exception('Ошибка действий 13')
        time.sleep(5)
        
        # Определим - найдена ли улица однозначно
        els_div = driver.find_elements(By.XPATH, '//div[@ng-hide="checkaddressAbstractController.loading"]')
        if len(els_div) > 0:  # Проблемма - улица не найдена или множественный выбор
            streets = []
            for el_div in els_div:
                if el_div.text == 'Улицы не найдены':
                    raise Exception(f'Ошибка Улица: {street} не найдена.')
            
            # Ищем всплывающее контекстное меню с подсказкой улиц
            els_div = driver.find_elements(By.ID, 'listStart')
            if len(els_div) != 1: raise Exception('Ошибка - нет всплывающее контекстное меню с подсказкой улицы')
            els_a = els_div[0].find_elements(By.XPATH, './/a[@class="link ng-binding"]')
            if len(els_a) == 0: raise Exception(f'Ошибка Улица: {street} не найдена2.')
            try: els_a[0].click()
            except: raise Exception('Ошибка действий 14')
            time.sleep(3)

        driver.implicitly_wait(10)
        time.sleep(3)
        
        # Ищем таблицу с номерами домов
        els_table = driver.find_elements(By.TAG_NAME, 'table')
        if len(els_table) != 1: raise Exception('Ошибка - нет таблицы домов')
        el_table = els_table[0]
        
        els_a = el_table.find_elements(By.TAG_NAME, 'a')
        if len(els_a) == 0: raise Exception('Ошибка В таблице домов нет элементов')
        
        house = data.get('house')
        if house: c_house = ordering_house(house)
        else: raise Exception('Ошибка не задан номер дома')
        
        if c_house[0] == '': raise Exception(f'Ошибка не распознан номер дома: \"{house}\"')
        el = None
        for el_a in els_a:
            if el_a.text == c_house[1]:
                el = el_a
                break
        if el:
            try: el.click()
            except: raise Exception('Ошибка действий 15')
        else: raise Exception(f'Ошибка Дом: {house} не найден')
        time.sleep(3)
        
        # Берем информацию об ограничениях по адресу
        info_restrictions = ''
        els = driver.find_elements(By.XPATH, '//div[@class="modal-content"]')
        if len(els) != 1: raise Exception('Ошибка нет всплывающего окна с информацией об ограничениях')
        els_b = els[0].find_elements(By.TAG_NAME, 'b')
        for el_b in els_b: info_restrictions += f'{el_b.text}\n'
        els_p = els[0].find_elements(By.TAG_NAME, 'p')
        for el_p in els_p: info_restrictions += f'{el_p.text}\n'
        
        # Жмем продолжить
        els_btn = driver.find_elements(By.XPATH, '//button[@ng-click="ok()"]')
        if len(els_btn) != 1: raise Exception('Ошибка нет кнопки продолжить после прочтения ограничений')
        try: els_btn[0].click()
        except: raise Exception('Ошибка действий 16')
        time.sleep(3)
        ###################### Страница ввода заявки ######################
        # Ищем квартиру
        apartment = data.get('apartment')
        if apartment:
            driver.set_window_size(300,800)
            time.sleep(2)
            
            els_ih = driver.find_elements(By.XPATH, '//input[@name="flat"]')
            if len(els_ih) < 2: raise Exception('Ошибка нет поля ввода квартиры')
            try: els_ih[1].send_keys(apartment)
            except: raise Exception('Ошибка действий 17')
            time.sleep(1)
            driver.set_window_size(1000,1000)
            time.sleep(1)
        
        # Вытаскиваем определившийся адрес
        els = driver.find_elements(By.XPATH, '//a[contains(@ui-sref, "checkaddress.address")]')
        # (By.XPATH, '//textarea[contains(@class, "SearchInput_textArea")]')
        if len(els) == 0: raise Exception('Ошибка нет полного адреса')
        data['pv_address'] = els[0].text
        
        # Жмем проверить
        els_btn = driver.find_elements(By.XPATH, '//button[@ng-click="$abonCtrl.checkAddress()"]')
        if len(els_btn) < 2: raise Exception('Ошибка нет кнопки проверить квартиру')
        try: els_btn[0].click()
        except: raise Exception('Ошибка действий 18')
        time.sleep(3)

        driver.implicitly_wait(1)
        # Проверяем блок если есть активный договор
        els_er = driver.find_elements(By.XPATH, '//div[@ng-if="$abonCtrl.addressErrorMessage"]')
        if els_er:
            err_txt = els_er[0].text
            if err_txt.find('На адресе есть активный договор') >= 0:
                data['available_connect'] = 'На адресе уже есть активный договор\n'
            else: raise Exception(f'Ошибка {err_txt}')
        time.sleep(3)

        # Смотрим тарифные планы
        # По умолчанию открыта вкладка "Все в одном"
        tarifs_all = '#Все в одном\n'
        # Ищем тарифные предложения
        els_tarifs = driver.find_elements(By.XPATH, '//label[@class="title cur-pointer ng-binding title--normal title--dotted"]')
        lst_tarif = []
        for el_tarif in els_tarifs:
            tarif = el_tarif.text.strip()
            if tarif: lst_tarif.append(tarif)
        tarifs_all += '\n'.join(lst_tarif)
        # Кликаем на  "Пакетные предложения"
        els_pack = driver.find_elements(By.XPATH, '//div[@ng-click="$servCtrl.stype.tab = 3; $servCtrl.stype.presetsClicked = true;"]')
        if len(els_pack) != 1: raise Exception('Ошибка - нет вкладки пакетные предложения')
        try: els_pack[0].click()
        except: raise Exception('Ошибка действий 19')
        time.sleep(5)
        tarifs_all += '\n#Пакетные предложения\n'
        # Ищем тарифные предложения
        els_tarifs = driver.find_elements(By.XPATH, '//label[@class="title cur-pointer ng-binding title--normal title--dotted"]')
        lst_tarif = []
        for el_tarif in els_tarifs:
            tarif = el_tarif.text.strip()
            if tarif: lst_tarif.append(tarif)
        tarifs_all += '\n'.join(lst_tarif)
        data['tarifs_all'] = tarifs_all
        
        # Жмем Просмотр графика подключений
        els_sp = driver.find_elements(By.XPATH, '//span[@ng-click="$abonCtrl.openScheduleHandler()"]')
        if len(els_sp) < 2: raise Exception('Ошибка нет ссылки Просмотр графика подключений')
        try: els_sp[0].click()
        except: raise Exception('Ошибка действий 20')
        time.sleep(3)
        
        driver.implicitly_wait(10)
        # Кликаем календарь
        els_inp = driver.find_elements(By.XPATH, '//input[@ng-model="$abonCtrl.schedule.date"]')
        if len(els_inp) != 1: raise Exception('Ошибка поля календарь')
        try: els_inp[0].click()
        except: raise Exception('Ошибка действий 21')
        time.sleep(1)
        
        els_btn_cld = driver.find_elements(By.XPATH, '//button[@ng-click="$abonCtrl.showCalendar()"]')
        if len(els_btn_cld) != 1: raise Exception('Ошибка нет кнопки календарь')
        try: els_btn_cld[0].click()
        except: raise Exception('Ошибка действий 22')
        time.sleep(3)
        
        els_cld = driver.find_elements(By.TAG_NAME, 'schedules-calendar')
        if len(els_cld) != 1: raise Exception('Ошибка нет блока календарь')
        
        # Определяем дату
        time.sleep(5)
        txt_months = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
        els_month = els_cld[0].find_elements(By.XPATH, './/div[@class="schedules-calendar"]')
        if len(els_month) == 0: raise Exception('Календарь не содержит блоки месяцев.')
        free_first_day = ''
        el_ff_day = None
        for el_month in els_month:
            f_month = False
            f_day = False
            els_tit_month = el_month.find_elements(By.XPATH, './/div[@class="schedules-calendar__caption title title--s title--normal ng-binding"]')
            if len(els_tit_month) != 1: raise Exception('Ошибка структуры календаря.Титул.')
            els_days_yellow = el_month.find_elements(By.XPATH, './/div[@class="schedules-calendar__day schedules-calendar__day--hover-border ng-binding ng-scope schedules-calendar__day--color-yellow"]')
            els_days_green = el_month.find_elements(By.XPATH, './/div[@class="schedules-calendar__day schedules-calendar__day--hover-border ng-binding ng-scope schedules-calendar__day--color-green"]')
            els_days = els_days_yellow + els_days_green
            try:
                els_days.sort(key=lambda x: int(x.text))
            except:
                pass
            for el_days in els_days:
                if free_first_day == '':
                    el_ff_day = el_days
                    free_first_day = f'{el_days.text} {els_tit_month[0].text}'
                    break

        if free_first_day:
            try: el_ff_day.click()
            except: raise Exception('Ошибка действий 23')
            time.sleep(5)
        
            # Смотрим время
            els_time = driver.find_elements(By.XPATH, '//span[@class="ui-select-toggle"]')
            if len(els_time) != 1: raise Exception('Ошибка: Нет поля выбора время.')
            try: els_time[0].click()
            except: raise Exception('Ошибка действий 24')
            time.sleep(2)
            
            els_li_times = driver.find_elements(By.XPATH, '//li[@id="ui-select-choices-0"]')
            if len(els_li_times) != 1: raise Exception('Ошибка: Нет блока время.')
            els_times = els_li_times[0].find_elements(By.XPATH, './/span[@class="ng-binding ng-scope"]')
            if len(els_times) == 0: raise Exception('Ошибка: Нет вариантов выбора время.')

            lst_tmp = []
            available_timeslot = ''
            try:
                for el_times in els_times:
                    l_time = el_times.text.strip()
                    ll_time = l_time.split(' — ')
                    t1_t = ll_time[0].split(':')
                    t2_t = ll_time[1].split(':')
                    lst_tmp.append(f'{t1_t[0]}-{t2_t[0]}')
            except: raise Exception('Ошибка сбора списка времени.')
            if lst_tmp: available_timeslot = ';'.join(lst_tmp)
            data['available_connect'] += f'Возможно подключение {free_first_day}\n в {available_timeslot}\n'
        data['available_connect'] += info_restrictions

        # #===========
        # time.sleep(10)
        # with open('out_file.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========
        
    except Exception as e:
        return str(e), data
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
        'login': '0K23-181',
        'password': 'CgslU7tfFsK5w8',
        'id_lid': '1215557',
        'city': 'Ярославль',
        'street': 'улица Труфанова',
        'house': '29 корп 3',
        'apartment': '65',
        'region': 'Яроа'
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

    url = 'https://crm.domconnect.ru/rest/371/ao3ct8et7i7viajs/crm.lead.update'
    # Данные для СРМ
    
    # 'info_restrictions': '',
    # 'tarifs_all': '',
    # 'contract': '',
    # 'find_date': '',
    # 'available_first_date_connect': '',
    # 'available_timeslot': '',
    
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
    
    params = {
        'id': txv_dict.get('id_lid'),
        'fields[UF_CRM_1638779781554][]': restrictions[:500],  # вся инфа
    }

    try:
        responce = requests.post(url, headers=headers, params=params)
        st_code = responce.status_code
        if st_code != 200: return st_code
        # посмотреть результат https://crm.domconnect.ru/crm/lead/details/1215557/
    except Exception as e:
        return str(e)
    
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

def run_txv_beeline(tlg_chat, tlg_token):
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

    # Перелистываем список словарей с запросами
    for txv_dict in txv_list:
        rez, data = get_txv(txv_dict)
        data['bot_log'] = rez
        crm = send_crm_txv(data, opsos)  # ответ в CRM
        crm_mess = f'Ошибка при отправке в СРМ: {crm}\n'
        if crm:
            tlg_mess += crm_mess
            data['bot_log'] += crm_mess
        address = f'{data.get("city")} {data.get("street")} д.{data.get("house")} кв.{data.get("apartment")}'
        tlg_mess += f'{opsos}: - Выполнен запрос ТхВ\n'
        tlg_mess += f'Адрес: {address}\n'
        djdc = ''
        if rez == '':  # заявка успешно создана
            djdc = set_txv_status(3, data)
            tlg_mess += 'Успешно.\n'
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
    
    # https://partnerweb.beeline.ru
    # set_txv_to_dj_domconnect(pv_code)
    
    
    # rez, txv_list = get_txv_in_dj_domconnect(pv_code)
    # for val in txv_list:
        # print(val)
    
    # # Красногорск	Красногорский бульвар	8
    # data = {
        # 'login': 'S24-61',
        # 'password': 'Gf&dhdk234hfbbs4',
        # 'pv_code': pv_code,

        # 'city': 'Красногорск',
        # # 'street': 'улица Труфанова',
        # # 'house': '29 корп 3',
        # # 'apartment': '65',
        # 'street': 'Красногорский бульвар',
        # 'house': '8',
        # 'apartment': '20',
        
        # 'available_connect': '',  # Возможность подключения
        # 'tarifs_all': '', # список названий тарифных планов
        # 'pv_address': '',
    # }
    # rez, data = get_txv(data)
    # if rez: print(rez)

    # print('available_connect:', data['available_connect'])
    # print('pv_address:', data['pv_address'])
    # print('tarifs_all:')
    # print(data['tarifs_all'])
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # print(time_str)
    # limit_request_line

    
    
    pass
    '''
        1 аккаунт
            S24-61
            1010000101
            Gf&dhdk234hfbbs4

        2 аккаунт
            0K23-181
            1010000101
            CgslU7tfFsK5w8
    '''