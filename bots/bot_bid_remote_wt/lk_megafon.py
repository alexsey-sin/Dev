import os, json, time, requests  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

opsos = 'megafon'

# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

emj_red_mark = '❗️'
emj_red_ball = '🔴'
emj_yellow_ball = '🟡'
emj_green_ball = '🟢'
emj_red_rhomb = '♦️'
emj_yellow_rhomb = '🔸'

# личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# общий канал бот @Domconnect_bot Парсинг ЛК       LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN
LK_TELEGRAM_CHAT_ID = '-1001580291081'
LK_TELEGRAM_TOKEN = '526322367:AAEaw2vaeLl_f6Njfb952NopyxqCGRQXji8'


def get_access_in_dj_domconnect(op_name):
    url = url_host + 'api/get_lk_access'
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    params = {
        'key': 'Q8kGM1HfWz',
        'lk_name': op_name,
    }
    
    try:
        responce = requests.get(url, headers=headers, params=params)
    except:
        return 1, {}
    if responce.status_code == 200:
        acc_dct = json.loads(responce.text)
        return 0, acc_dct
    return 2, {}

def wait_spinner_points(driver):  # Ожидаем спинер с точками
    driver.implicitly_wait(1)
    while True:
        time.sleep(1)
        els = driver.find_elements(By.XPATH, '//div[contains(@class, "loader__frame")]')
        if len(els):
            pass
            # print('loader__frame')
        else: break
    driver.implicitly_wait(10)
    time.sleep(2)

def run_lk_parsing(access):
    # https://b2blk.megafon.ru/login		9201337110	dkk3D2
    driver = None
    try:
        base_url = 'https://b2blk.megafon.ru'
        EXE_PATH = 'driver/chromedriver.exe'
        service = Service(EXE_PATH)
        driver = webdriver.Chrome(service=service)

        driver.implicitly_wait(10)
        driver.get(base_url + '/login')
        time.sleep(3)

        login = access.get('login')  # '9201337110'
        password = access.get('password')  # 'dkk3D2'
        
        els = driver.find_elements(By.XPATH, '//input[@data-input-login="loginAuthform"]')
        if len(els) != 1: raise Exception('Нет поля логин')
        try: els[0].send_keys(login)
        except: raise Exception('Ошибка действий 1')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@data-input-pwd="passwordAuthform"]')
        if len(els) != 1: raise Exception('Нет поля пароль')
        try: els[0].send_keys(password)
        except: raise Exception('Ошибка действий 2')
        time.sleep(1)
        
        els = driver.find_elements(By.XPATH, '//button[@data-button="buttonSubmitAuthform"]')
        if len(els) != 1: raise Exception('Нет кнопки вход')
        try: els[0].click()
        except: raise Exception('Ошибка действий 3')
        
        # Ждем спинер
        wait_spinner_points(driver)
        time.sleep(1)

        ###################### Главная страница ######################
        
        els = driver.find_elements(By.CLASS_NAME, 'widget-personal-account__current-balance')
        if len(els) != 1: raise Exception('Определение баланса1')
        els1 = els[0].find_elements(By.CLASS_NAME, 'widget-personal-account__balance-text')
        if len(els1) != 1: raise Exception('Определение баланса2')

        str_balance = els1[0].text.strip().split()[0]
        data = {
            'operator': 'megafon',
            'balance': str_balance,
            'numbers': [],
        }
        
        # переходим на страницу абоненты
        driver.get(base_url + '/subscribers/mobile')
        time.sleep(10)

        ###################### Абоненты ######################
        els = driver.find_elements(By.XPATH, '//div[@data-col-name="msisdn"]')
        if len(els) < 2: raise Exception(6)
        dct_nums = {}
        for i in range(1, len(els)):
            el = els[i].find_elements(By.TAG_NAME, 'a')
            if len(el) != 1: raise Exception(7)
            dct_nums[el[0].text] = el[0].get_attribute('href')

        ###################### Перебираем страницы абонентов ######################
        for key, value in dct_nums.items():
            driver.get(value)  # value = типа: https://b2blk.megafon.ru/subscriber/info/124701207
            
            # Ждем спинер
            wait_spinner_points(driver)
            time.sleep(5)

            str_number = key.strip().replace(' ','').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
            number = {'number': str_number, }
            
            try:
                # Ищем блок с опциями тарифного плана
                driver.implicitly_wait(1)
                els_block = driver.find_elements(By.XPATH, '//div[contains(@class, "subscriber-id-info__tariff-discounts")]')
                if len(els_block) != 1: raise Exception()  # 'Нет блока с опциями тарифного плана'

                # Раскроем список
                els_open = els_block[0].find_elements(By.XPATH, './/span[contains(@class, "eSRigz link")]')
                if len(els_open) != 1: raise Exception('Нет списока с опциями тарифного плана')
                try: driver.execute_script("arguments[0].click();", els_open[0])
                except: raise Exception('Раскрытие списка')
                time.sleep(3)

                # Переберем строки с опциями тарифа
                els_opt = els_block[0].find_elements(By.XPATH, './/div[contains(@class, "subscriber-id-info__range")]')
                for el_opt in els_opt:
                    els_tit = el_opt.find_elements(By.XPATH, './/div[contains(@class, "arrow-tooltip__text")]')
                    if len(els_tit) != 1: raise Exception('2')
                    els_val = el_opt.find_elements(By.XPATH, './/div[contains(@class, "progress-bar__title-right")]')
                    if len(els_val) != 1: raise Exception('3')
                    
                    str_tit = els_tit[0].text
                    str_val = els_val[0].text
                    if str_tit.find('Минут') >= 0:
                        lst_val = str_val.split(' ')
                        number['mobile_available'] = lst_val[0]
                        number['mobile_total'] = lst_val[2]
                    if str_tit.find('SMS') >= 0:
                        lst_val = str_val.split(' ')
                        number['sms_available'] = lst_val[0]
                        number['sms_total'] = lst_val[2]
            except Exception as e: print(e)
            data['numbers'].append(number)

        ###################### Вывод ######################
        buff = f'Parsing {data.get("operator")}:\n'
        str_bal = data.get("balance")
        emj = ''
        if str_bal:
            str_bal = str_bal.replace(',', '.')
            bal = float(str_bal)
            if bal < 100: emj = emj_yellow_ball
            if bal <= 0: emj = emj_red_ball
        else: bal = '---'
        buff += f'{emj}balance: {bal}\n'
        nums = data.get('numbers')
        cnt_nums = len(nums)
        cnt_avlb_min = 0
        cnt_avlb_sms = 0
        
        for dct in nums:
            str_number = dct.get('number')
            str_avlb_min = dct.get('mobile_available')
            str_totl_min = dct.get('mobile_total')
            str_avlb_sms = dct.get('sms_available')
            str_totl_sms = dct.get('sms_total')
            try:
                emj = ''
                avlb_min = int(str_avlb_min)
                totl_min = int(str_totl_min)
                avlb_sms = int(str_avlb_sms)
                totl_sms = int(str_totl_sms)
                if avlb_min == 0 and avlb_sms == 0: continue
                if avlb_min < 500: emj = emj_yellow_rhomb
                if avlb_min < 100: emj = emj_red_rhomb
                cnt_avlb_min += avlb_min
                cnt_avlb_sms += avlb_sms
                
                buff += f'{emj}{str_number} [min {avlb_min}/{totl_min}][sms {avlb_sms}/{totl_sms}]\n'
            except: continue
        buff += f'Итого: [min {cnt_avlb_min}][sms {cnt_avlb_sms}]\n'
        buff += f'Всего номеров: {cnt_nums}\n'
    except Exception as e:
        return str(e)[:100], {}, ''
    finally:
        if driver: driver.quit()

    # #===========
    # # time.sleep(10)
    # with open('out_lk.html', 'w', encoding='utf-8') as outfile:
        # outfile.write(driver.page_source)
    # raise Exception('Финиш.')
    # #===========
    ###################### Формируем POST запрос в базу данных ######################
    '''
    структура отправляемых данных:
    data = {
        'operator': 'megafon',
        'balance': '-127,73',
        'numbers': [
            {
                'number': '+7(961)161-25-00',
                'mobile_available': '23',
                'mobile_total': '467',
                'sms_available': '0',
                'sms_total': '0',
            },
            {
                'number': '+7(961)161-17-00',
            },
            ...
        ]
    }

    '''
    ###################### Всем спасибо, все свободны ######################
    return '', data, buff

def send_telegram(chat: str, token: str, text: str):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try: requests.post(url, data={'chat_id': chat, 'text': text})
    except: print('ERROR telegram send message.')

def send_api(data):
    # API_MOBILE_URL = 'http://127.0.0.1:8000/mobile/api'
    # BSE_URL = 'http://127.0.0.1:8000/'

    API_MOBILE_URL = 'http://37.46.128.40/mobile/api'
    BSE_URL = 'http://37.46.128.40/'

    try:
        client = requests.session()
        resp = client.get(BSE_URL)
        csrftoken = resp.cookies.get('csrftoken')
        header = {
            "Content-type": "application/json",
            "X-CSRFToken": csrftoken,
        }
        resp = client.post(API_MOBILE_URL, headers=header, json=data)
    except: return f'Parsing {opsos} Error send API'

    return ''

def run_lk_megafon(chat, token):
    print(f'Start parsing {opsos}')

    # Получаем доступы
    e, access = get_access_in_dj_domconnect(opsos)
    if e:
        mess = f'run_lk_{opsos} ERROR get_access: {e}'
        send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
        logger.error(mess)
        return
    if access == {}: return
    time.sleep(1)

    tlg_mess = ''
    e, data, mess = run_lk_parsing(access)
    if e:
        tlg_mess = f'Parsing {opsos} - ERROR: {e}'
    else:
        e = send_api(data)
        if e: tlg_mess = e
        else: tlg_mess = mess
    send_telegram(chat, token, tlg_mess)
    print(tlg_mess)
        
        
if __name__ == '__main__':
    
    run_lk_megafon(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)  # В личный infra чат
    # run_lk_megafon(LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN)  # В общий чат
