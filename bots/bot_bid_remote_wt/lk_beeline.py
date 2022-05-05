import os, json, time, requests  # pip install requests
from datetime import datetime
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.firefox.service import Service
# from selenium.webdriver.firefox.options import Options

opsos = 'beeline'

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
    # https://my.beeline.ru		S715792964	MuE8$lVGpo
    driver = None
    try:
        base_url = 'https://my.beeline.ru'
        EXE_PATH_Ch = 'driver/chromedriver.exe'
        # EXE_PATH_Fx = 'driver/geckodriver.exe'

        # cnt = 5
        # while cnt:
            # cnt -= 1
            # try:
                # print(f'try: {5-cnt}')
                # time.sleep(1)
        # options = Options()
        # options.binary_location = r'C:\Users\asinicin\AppData\Local\Mozilla Firefox\firefox.exe'
        # options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
        # driver = webdriver.Firefox(service=Service(EXE_PATH_Fx), options=options)
        service = Service(EXE_PATH_Ch)
        driver = webdriver.Chrome(service=service)
        driver.implicitly_wait(10)
        driver.get(base_url)
        time.sleep(3)
        ###################### Login ######################
        login = access.get('login')  # 'S715792964'
        password = access.get('password')  # 'MuE8$lVGpo'
        
        els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:login')
        # if len(els) != 1: continue
        if len(els) != 1: raise Exception('login 1')
        els[0].send_keys(login)
        time.sleep(3)

        els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:passwordPwd')
        if len(els) != 1: raise Exception('login 2')
        els[0].send_keys(password)
        time.sleep(1)
        els[0].send_keys(Keys.ENTER)
        time.sleep(5)

        # els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:loginButton')
        # if len(els) != 1: raise Exception('login 3')
        # driver.execute_script("arguments[0].click();", els[0])
        # # els[0].click()
        # time.sleep(5)
                # break
            # except Exception as e:
                # print(e)
                # continue
        ###################### Главная страница ######################

        driver.get(base_url + '/b/info/abonents/catalog.xhtml')
        time.sleep(5)
        ###################### Абоненты страница ######################

        els_div = driver.find_elements(By.ID, 'mobileDataForm:abonents')
        if len(els_div) != 1: raise Exception(1)
        el_div = els_div[0]

        num_urls = []
        driver.implicitly_wait(0)
        while True:
            time.sleep(3)
            # собираем ссылки
            ts_body = el_div.find_elements(By.ID, 'mobileDataForm:abonents_data')
            if len(ts_body) != 1: raise Exception(2)
            t_body = ts_body[0]
            trs = t_body.find_elements(By.TAG_NAME, 'tr')
            for tr in trs:
                els_act = tr.find_elements(By.CLASS_NAME, 'reason')
                if len(els_act) != 1: raise Exception(3)
                el_act = els_act[0]
                active = el_act.text
                if active.find('Активен') >= 0:
                    tds = tr.find_elements(By.TAG_NAME, 'td')
                    for td in tds:
                        els_a = td.find_elements(By.TAG_NAME, 'a')
                        if len(els_a) == 1:
                            link = els_a[0].get_attribute('href')
                            if link.find('/b/info/subscriberDetail.xhtml?objId=') >= 0:
                                num_urls.append(link)

            # анализируем паджинатор
            els_next = el_div.find_elements(By.XPATH, "./*//a[@aria-label='Next Page']")
            if len(els_next) != 1: raise Exception(4)
            el_next = els_next[0]

            s_cl = el_next.get_attribute('class')
            if s_cl.find('ui-state-disabled') >= 0:
                break
            else:
                el_next.click()

        ###################### Страницы каждого абонента ######################
        data = {
            'operator': opsos,
            'numbers': [],
        }
        # num_urls = [
        #     'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=3035129841',
        #     'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2043457941',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2043457942',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2043457973',
        #     'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2093908483',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2093909663',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2043457944',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2043457947',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=2093906797',
        #     # 'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=3035128790',
        #     'https://my.beeline.ru/b/info/subscriberDetail.xhtml?objId=3035127310',
        #     ]
        for link in num_urls:
            driver.implicitly_wait(20)
            driver.get(link)
            time.sleep(10)

            els_num = driver.find_elements(By.XPATH, "//span[@class='has-subheader']")
            if len(els_num) != 1: raise Exception(5)
            str_number = '7' + els_num[0].text.strip().replace(' ','').replace('(', '').replace(')', '').replace('-', '')
            str_number = str_number
            number = {'number': str_number, 'mobile_available': 0, 'mobile_packet': 0, 'sms_available': 0, 'sms_packet': 0}
            driver.implicitly_wait(0)

            # находим блок с "А еще у вас есть"
            els_divblok = driver.find_elements(By.XPATH, "//div[@class='bonuses-accums-list']")
            if len(els_divblok) != 1: raise Exception(6)
            el_divblok = els_divblok[0]

            # перелистываем вложенные div-ы
            els_divs = el_divblok.find_elements(By.TAG_NAME, 'div')
            if len(els_divs) < 8:  # значит пустые
                data['numbers'].append(number)
                continue
            
            # перелистываем строчки
            for el_divs in els_divs:
                class_name = el_divs.get_attribute('class')
                if class_name.find('accum-restyle') < 0:
                    continue
                
                label = ''
                value = ''
                els_divs_accum = el_divs.find_elements(By.TAG_NAME, 'div')
                for el_divs_accum in els_divs_accum:
                    name_class = el_divs_accum.get_attribute('class')
                    if name_class.find('column1') >= 0:
                        label = el_divs_accum.text.strip()
                    if name_class.find('column2') >= 0:
                        try:
                            el_val = el_divs_accum.find_element(By.TAG_NAME, 'div')
                            value = el_val.text.strip()
                        except: pass

                if len(label) > 0 and len(value) > 0:
                    lst_val = value.split()
                    bal = lst_val[1].strip()
                    tot = lst_val[4].strip()
                    balance = total = 0
                    try:
                        balance = int(bal)
                        total = int(tot)
                    except: continue
                    if balance == 100 and total == 100: continue
                    if label.find('Мобильная связь') >= 0:
                        number['mobile_available'] += balance
                        number['mobile_packet'] += total
                    if label.find('SMS') >= 0:
                        number['sms_available'] += balance
                        number['sms_packet'] += total
            data['numbers'].append(number)
        ###################### Вывод ######################
        buff = f'Parsing {data.get("operator")}:\n'
        nums = data.get('numbers')
        cnt_nums = len(nums)
        cnt_avlb_min = 0
        cnt_totl_min = 0
        cnt_avlb_sms = 0
        cnt_totl_sms = 0
        
        for dct in nums:
            str_number = dct.get('number')
            avlb_min = dct.get('mobile_available')
            totl_min = dct.get('mobile_packet')
            avlb_sms = dct.get('sms_available')
            totl_sms = dct.get('sms_packet')

            if avlb_min == 0 and totl_min == 0 and avlb_sms == 0 and totl_sms == 0: continue
            
            cnt_avlb_min += avlb_min
            cnt_totl_min += totl_min
            cnt_avlb_sms += avlb_sms
            cnt_totl_sms += totl_sms
            
            emj = ''
            if avlb_min < 500: emj = emj_yellow_rhomb
            if avlb_min < 100: emj = emj_red_rhomb
            sub_str = f'{emj}{str_number} [min {avlb_min}/{totl_min}]'

            if avlb_sms or totl_sms:
                sub_str += f'[sms {avlb_sms}/{totl_sms}]'
            
            buff += sub_str + '\n'

        buff += f'Итого: [min {cnt_avlb_min}/{cnt_totl_min}][sms {cnt_avlb_sms}/{cnt_totl_sms}]\n'
        buff += f'Всего номеров: {cnt_nums}\n'
    except Exception as e:
        return str(e)[:100], {}, ''
    finally:
        try: driver.quit()
        except: pass

        # with open('out.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Finish')

    ###################### Формируем POST запрос в базу данных ######################
    '''
    структура отправляемых данных:
    data = {
        'operator': 'beeline',
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

def run_lk_beeline(chat, token):
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
    
    run_lk_beeline(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)  # В личный infra чат
    # run_lk_beeline(LK_TELEGRAM_CHAT_ID, LK_TELEGRAM_TOKEN)  # В общий чат


    # https://yaroslavl.beeline.ru/customers/products/mobile/profile/#/home
    # 7 962 208-70-00
    # MnIAarB78R
