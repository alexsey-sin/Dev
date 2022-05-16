import os, time, re, json
from datetime import datetime, timedelta
import calendar, requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


provider = 'РТК'
pv_crm_code = 3
# личный бот @infra
MY_TELEGRAM_CHAT_ID = '1740645090'
MY_TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

access = {  # Доступы к ПВ
    'url': 'https://eissd.rt.ru/login',
    'login': 'sz_v_an',
    'password': 'm~|HqEu~VB}|P1QDrDX%'
}
status_rtk_srm = {  # Коды статусов: РТК = СРМ
    'Услуга подключена': 2,  # Подключен
    'Отказ': 'NEW',  # Ошибки + коммент
    'Дубликат': 'NEW',  # Ошибки + коммент
    'Неверная заявка': 'NEW',  # Ошибки + коммент
    'Тест': 11,  # Служебный
    'Продажа оборудования': 2,  # Подключен
    'Самоинсталляция / Доставка оборудования курьером, 0/1': 2,  # Подключен
}
status_for_comment = [  # Статусы РТК когда требуется взять коментарий из истории
    'Отказ',
    'Дубликат',
    'Неверная заявка',
]


def get_deals_crm(pv, from_data, to_date):
    url = 'https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.list'
    
    go_next = 0
    go_total = 0
    out_lst = []

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    while True:
        data = {
            'start': go_next,
            'order': {'ID': 'ASC'},  # Если нужно с сортировкой
            'filter': {
                '>=DATE_CREATE': from_data,  # '2021-10-01T00:00:00'
                '<DATE_CREATE': to_date,  # '2021-10-01T00:00:00'
                'UF_CRM_5903C16B84C55': pv,  # Провайдер
                'STAGE_ID': [1, 5],
                'UF_CRM_595E343AA0EE2': 0,  # Юр. лицо
            },
            'select': [
                'ID',
                'DATE_CREATE',
                'STAGE_ID',
                'UF_CRM_5903C16BDF7A7',  # Номер заявки
                'UF_CRM_595ED493B6E5C',  # PartnerWEB
            ]
        }
        try:
            responce = requests.post(url, headers=headers, json=data)
            if responce.status_code == 200:
                answer = json.loads(responce.text)
                result = answer.get('result')
                go_next = answer.get('next')
                go_total = answer.get('total')
                out_lst += result
                if not go_next: break
                print(go_next, go_total)
            else:
                return f'Ошибка get_deals: responce.status_code: {responce.status_code}\n{responce.text}', []
        except:
            return 'Ошибка get_deals: try: requests.post', []
        time.sleep(1)
    return '', out_lst
    # https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.list?
    # order[id]=DESC&filter[>DATE_CREATE]=2022-03-01&filter[UF_CRM_5903C16B84C55]=3&filter[STAGE_ID]=1&filter[UF_CRM_595E343AA0EE2]=0&select[]=UF_CRM_5903C16BDF7A7&select[]=STAGE_ID&select[]=DATE_CREATE&select[]=UF_CRM_595ED493B6E5C
    pass

def wait_spinner(driver):  # Ожидаем крутящийся спинер
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-spinner")]')
        if len(els):
            # print('ju-spinner')
            pass
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

def get_deal_status(lst_deal, access, status_for_comment):
    driver = None
    try:
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
        # driver = webdriver.Firefox(executable_path=EXE_PATH)

        driver.implicitly_wait(10)
        driver.get(access.get('url'))
        time.sleep(3)
        
        # ###################### Login ######################
        login = access.get('login')
        if login:
            els = driver.find_elements(By.XPATH, '//input[@data-field="login"]')
            try: els[0].send_keys(login)
            except: raise Exception('Ошибка ввода логин')
            time.sleep(1)
        else: raise Exception('Ошибка не задан логин')

        password = access.get('password')
        if password:
            els = driver.find_elements(By.XPATH, '//input[@data-field="passw"]')
            try: els[0].send_keys(password)
            except: raise Exception('Ошибка ввода пароля')
            time.sleep(2)
        else: raise Exception('Ошибка не задан пароль')

        els = driver.find_elements(By.XPATH, '//input[@data-field="closeOthers"]')
        # Обычным способом чекбокс не отмечается - element not interactable
        try: driver.execute_script("arguments[0].click();", els[0])
        except: raise Exception('Ошибка отметки чекбокса закрыть другие сессии')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@value="Войти"]')
        try: els[0].click()
        except: raise Exception('Ошибка нажатия кнопки авторизации')
        time.sleep(1)
        
        wait_spinner(driver)  # Подождем если есть спинер
        
        driver.implicitly_wait(1)
        els = driver.find_elements(By.XPATH, '//div[@class="form-group error"]')
        if els: raise Exception(f'Ошибка {els[0].text}')  # Неверное имя пользователя или пароль
        driver.implicitly_wait(10)
        ###################### Главная страница ######################
        els = driver.find_elements(By.XPATH, '//a[@href="/order/phys/list"]')
        if len(els) < 2: raise Exception('Нет ссылки Расширенный поиск заявок ФЛ')
        try: els[1].click()
        except: raise Exception('Ошибка клика ссылки перехода на страницу поиска заявки')
        time.sleep(3)
        ###################### Страница поиска заявки ######################
        # проверим всплывашки с рекламой
        driver.implicitly_wait(2)
        els = driver.find_elements(By.XPATH, '//div[@class="ju-popup ju-message user-messages-popup "]')
        for el in els:
            els_btn = el.find_elements(By.TAG_NAME, 'input')
            try: driver.execute_script("arguments[0].click();", els_btn[0])
            except: raise Exception('Ошибка закрытия окна всплывашки с рекламой')
            time.sleep(1)
        driver.implicitly_wait(10)

        # проход по всем заявкам
        for deal in lst_deal:
            deal['status'] = ''
            num = deal.get('num')
            if not num: continue
            els = driver.find_elements(By.XPATH, '//input[@name="packetNum"]')
            if len(els) != 1: raise Exception('Нет поля ввода номера заявки')
            # вводим номер заявки
            try:
                els[0].send_keys(Keys.CONTROL + 'a')
                time.sleep(1)
                els[0].send_keys(Keys.DELETE)
                time.sleep(1)
                els[0].send_keys(num)
            except: raise Exception('Ошибка ввода номера заявки')
            time.sleep(1)
            els = driver.find_elements(By.XPATH, '//input[contains(@class, "def-tabs-apply")]')
            if len(els) == 0: raise Exception('Нет кнопки поиска заявки')
            try: els[0].click()
            except: raise Exception('Ошибка клика кнопки поиска заявки')
            wait_spinner(driver)  # Подождем если есть спинер
            time.sleep(1)
            # Проверим нет ли всплывающего окна с сообщением
            driver.implicitly_wait(2)
            els = driver.find_elements(By.XPATH, '//div[contains(@class, "ju-popup ju-message attention")]')
            if len(els) == 1:
                els_cont = els[0].find_elements(By.XPATH, './/div[@class="content"]')
                if len(els_cont) > 0: deal['status'] = els_cont[0].text
                els_btn = els[0].find_elements(By.XPATH, './/input[contains(@class, "close")]')
                if len(els_btn) > 0:
                    try: els_btn[0].click()
                    except: raise Exception('Ошибка клика закрыть сообщение')
                time.sleep(2)
                continue
            # Посмотрим результат
            status = ''
            date_connect = ''  # Дата подключения
            els_div = driver.find_elements(By.XPATH, '//div[@id="filter_result"]')
            if len(els_div) == 0: raise Exception('Нет блока результатов поиска заявки')
            els_tbody = els_div[0].find_elements(By.TAG_NAME, 'tbody')
            if len(els_tbody) == 0: raise Exception('Нет таблицы результатов поиска заявки')
            els_tr = els_tbody[0].find_elements(By.TAG_NAME, 'tr')
            if len(els_tr) == 0: raise Exception('Нет строк таблицы результатов поиска заявки')
            for el_tr in els_tr:
                els_td = el_tr.find_elements(By.TAG_NAME, 'td')
                if len(els_td) != 14: raise Exception('Неправильный формат строки таблицы результатов поиска заявки')
                # Сравниваем статусы по строкам
                # В работу берем только если статусы по всем строкам одинаковые
                if status == '':
                    status = els_td[7].text
                    date_connect = els_td[8].text
                    continue
                else:
                    if status != els_td[7].text:  # Разные статусы по строкам
                        status = 'varied status'
                        break
                
            if status: deal['status'] = status
            if date_connect: deal['date_connect'] = date_connect
            try:
                if status in status_for_comment:
                    els_td = els_tr[0].find_elements(By.TAG_NAME, 'td')
                    els_a = els_td[13].find_elements(By.TAG_NAME, 'a')
                    els_a[0].click()
                    wait_spinner(driver)  # Подождем если есть спинер
                    time.sleep(1)
                    els_div_his = driver.find_elements(By.XPATH, '//div[contains(@class, "status-history-dialog")]')
                    els_tr = els_div_his[0].find_elements(By.TAG_NAME, 'tr')
                    els_td = els_tr[-1].find_elements(By.TAG_NAME, 'td')
                    comment = els_td[6].text
                    if comment.isdigit(): deal['comment'] = status
                    else: deal['comment'] = comment
                    # Закрываем
                    els_btn = els_div_his[0].find_elements(By.XPATH, './/input[contains(@class, "close")]')
                    if len(els_btn) > 0: els_btn[0].click()
                    time.sleep(1)
            except Exception as e: print(e)
        
        
        #===========
        # time.sleep(10)
        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        #===========

    

    except Exception as e:
        return str(e)[:100], lst_deal
    finally:
        if driver: driver.quit()
   
    return '', lst_deal

def send_crm_deal_stage(deal, new_code_stage):
    url = 'https://crm.domconnect.ru/rest/371/w95d249i00jagfkv/crm.deal.update'
    # HELP: https://dev.1c-bitrix.ru/rest_help/crm/cdeals/crm_deal_update.php

    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    
    # Собираем данные
    data = {
        'id': deal.get('ID'),
        'fields': 
            {
                'STAGE_ID': new_code_stage,
            }
    }
    comment = deal.get('comment')
    if comment: data['fields']['UF_CRM_59B40B8474D0A'] = comment
    if new_code_stage == 2: data['fields']['UF_CRM_5904FB99DBF0C'] = deal.get('date_connect', '')
    
    # Отсылаем
    try:
        responce = requests.post(url, headers=headers, json=data)
        st_code = responce.status_code
        if st_code != 200: return st_code
    except Exception as e:
        return str(e)
        
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

def run_check_deals(tlg_chat, tlg_token, by_days=60):
    tlg_mess = ''

    # Определим диапазон дат для фильтра
    cur_date = datetime.today()
    to_date = cur_date.date()
    from_date = (cur_date - timedelta(days=by_days)).date()
    
    # Заберем сделки из СРМ по фильтру
    e, lst_deal = get_deals_crm(pv_crm_code, str(from_date), str(to_date))
    if e: 
        tlg_mess = f'ПВ {provider}: Ошибка при загрузке сделок из срм'
        r = send_telegram(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    if len(lst_deal) == 0:
        cur_time = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
        print(f'{cur_time} {provider}: Сделок нет')
        return

    print('Исходный список:', len(lst_deal), 'шт.')
    # Соберем нормальный список сделок
    new_lst_deal = []
    for dl in lst_deal:
        num = dl.get('UF_CRM_5903C16BDF7A7')
        id_d = dl.get('ID')
        l_sub = re.findall('\d{13}', str(num))
        if len(l_sub) == 1: new_lst_deal.append({'ID': id_d, 'num': l_sub[0]})
        else:
            l_sub = re.findall('\d{12}', str(num))
            if len(l_sub) == 1 and num.find('100') == 0:
                new_lst_deal.append({'ID': id_d, 'num': f'1{l_sub[0]}', 'correct': 'True'})
    print('Нормализованный список:', len(new_lst_deal), 'шт.')
    
    # Проверим статус сделок у ПВ
    e, lst_deal = get_deal_status(new_lst_deal, access, status_for_comment)
    if e: 
        tlg_mess = f'ПВ {provider}: Ошибка при проверке статуса сделок: {e} '
        r = send_telegram(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, tlg_mess)
        print(tlg_mess, '\nTelegramMessage:', r)
        return
    
    change = 0
    for deal in lst_deal:
        status = deal.get('status')
        if status and status in status_rtk_srm:
            print(deal.get('ID'), status, status_rtk_srm[status])
            e = send_crm_deal_stage(deal, status_rtk_srm[status])
            if e: 
                tlg_mess = f'ПВ {provider}: Ошибка при обновлении статуса сделки в срм'
                r = send_telegram(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, tlg_mess)
                print(tlg_mess, '\nTelegramMessage:', r)
            else: change += 1
            time.sleep(1)
    
    tlg_mess = f'ПВ {provider}:\nСтатус сделок изменен\nв {change} из {len(lst_deal)}'
    r = send_telegram(tlg_chat, tlg_token, tlg_mess)
    print(tlg_mess, '\nTelegramMessage:', r)


if __name__ == '__main__':
    # run_check_deals(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN, 1)
    run_check_deals(MY_TELEGRAM_CHAT_ID, MY_TELEGRAM_TOKEN)

    pass