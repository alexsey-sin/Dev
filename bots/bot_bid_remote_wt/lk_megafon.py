import os, json, time, requests  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
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

def run_lk_parsing(access):
    # https://b2blk.megafon.ru/login		9201337110	dkk3D2
    driver = None
    try:
        base_url = 'https://b2blk.megafon.ru'
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url + '/login')
        time.sleep(3)

        login = access.get('login')  # '9201337110'
        password = access.get('password')  # 'dkk3D2'
        
        els = driver.find_elements(By.XPATH, '//input[@data-input-login="loginAuthform"]')
        if len(els) != 1: raise Exception(1)
        els[0].send_keys(login)
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@data-input-pwd="passwordAuthform"]')
        if len(els) != 1: raise Exception(2)
        els[0].send_keys(password)
        time.sleep(1)
        
        els = driver.find_elements(By.XPATH, '//button[@data-button="buttonSubmitAuthform"]')
        if len(els) != 1: raise Exception(3)
        els[0].click()
        time.sleep(10)

        ###################### Главная страница ######################
        # with open('out_file.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        
        els = driver.find_elements(By.CLASS_NAME, 'widget-personal-account__current-balance')
        if len(els) != 1: raise Exception(4)
        els1 = els[0].find_elements(By.CLASS_NAME, 'widget-personal-account__balance-text')
        if len(els1) != 1: raise Exception(5)

        str_balance = els1[0].text.strip().split()[0]
        data = {
            'operator': 'megafon',
            'balance': str_balance,
            'numbers': [],
        }

        # переходим на страницу абоненты
        driver.get(base_url + '/subscribers/mobile')
        time.sleep(30)
        ###################### Абоненты ######################
        # need_rows = 18  # (кол-во номеров + строка заголовка)
        # cnt = 0
        # while(1):
            # els = driver.find_elements(By.XPATH, '//div[@data-col-name="msisdn"]')
            # if len(els) >= need_rows:
                # break
            # else:
                # time.sleep(1)
            # if cnt > 25: raise Exception(6)
            # cnt += 1
        
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
            driver.implicitly_wait(2)
            time.sleep(5)

            str_number = key.strip().replace(' ','').replace('(', '').replace(')', '').replace('-', '').replace('+', '')
            number = {'number': str_number, }

            els = driver.find_elements(By.XPATH, '//div[@id="discountsList"]')
            if len(els) != 1: raise Exception(8)
            els_dl = els[0].find_elements(By.TAG_NAME, 'dl')
            if len(els_dl) == 0:
                data['numbers'].append(number)  
                continue

            for el_dl in els_dl:  # по блокам <dl>
                dts = el_dl.find_elements(By.TAG_NAME, 'dt')
                if len(dts) != 1: raise Exception(9)
                label = dts[0].text
                
                if label.find('SMS') >= 0:  # блок с 'SMS'
                    divs = el_dl.find_elements(By.TAG_NAME, 'div')
                    for div in divs:
                        dat = div.text
                        if dat.find('доступно') >= 0:
                            available = dat.split()[1]
                            number['sms_available'] = available

                elif label.find('Минут') >= 0:  # блок с 'Минут'
                    divs = el_dl.find_elements(By.TAG_NAME, 'div')
                    for div in divs:
                        dat = div.text
                        if dat.find('доступно') >= 0:
                            available = dat.split()[1]
                            number['mobile_available'] = available

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
            str_avlb_sms = dct.get('sms_available')
            try:
                emj = ''
                avlb_min = int(str_avlb_min)
                avlb_sms = int(str_avlb_sms)
                if avlb_min == 0 and avlb_sms == 0: continue
                if avlb_min < 500: emj = emj_yellow_rhomb
                if avlb_min < 100: emj = emj_red_rhomb
                cnt_avlb_min += avlb_min
                cnt_avlb_sms += avlb_sms
                
                buff += f'{emj}{str_number} [min {avlb_min}][sms {avlb_sms}]\n'
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
                'sms_available': '0',
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
