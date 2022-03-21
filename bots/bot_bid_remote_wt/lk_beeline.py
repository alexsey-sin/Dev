import os
import time
from datetime import datetime
import requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By

opsos = 'beeline'

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

def run_lk_parsing():
    # https://my.beeline.ru		S715792964	MuE8$lVGpo
    driver = None
    try:
        base_url = 'https://my.beeline.ru'
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url)
        time.sleep(5)
        ###################### Login ######################
        els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:login')
        if len(els) != 1: raise Exception('Ошибка: нет поля логин')
        els[0].send_keys('S715792964')
        time.sleep(1)

        els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:passwordPwd')
        if len(els) != 1: raise Exception('Ошибка: нет поля пароль')
        els[0].send_keys('MuE8$lVGpo')
        time.sleep(3)

        els = driver.find_elements(By.ID, 'loginFormB2C:loginForm:j_idt218')
        if len(els) != 1: raise Exception('Ошибка: нет кнопки вход')
        els[0].click()
        time.sleep(2)

        ###################### Главная страница ######################

        driver.get(base_url + '/b/info/abonents/catalog.xhtml')
        time.sleep(3)
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
            number = {'number': str_number, }
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
            mob = 1  # Будем брать только первую строчку "Мобильная связь"
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
                    balance = lst_val[1]
                    total = lst_val[4]
                    if label.find('Мобильная связь') >= 0 and mob:
                        mob = 0
                        number['mobile_available'] = balance
                        number['mobile_packet'] = total
                    if label.find('SMS') >= 0:
                        number['sms_available'] = balance
                        number['sms_packet'] = total
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
            str_avlb_min = dct.get('mobile_available')
            str_totl_min = dct.get('mobile_packet')
            str_avlb_sms = dct.get('sms_available')
            str_totl_sms = dct.get('sms_packet')
            try:
                avlb_min = totl_min = avlb_sms = totl_sms = 0
                
                if str_avlb_min: avlb_min = int(str_avlb_min)
                if str_totl_min: totl_min = int(str_totl_min)
                if str_avlb_sms: avlb_sms = int(str_avlb_sms)
                if str_totl_sms: totl_sms = int(str_totl_sms)
                
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
            except:
                continue
        buff += f'Итого: [min {cnt_avlb_min}/{cnt_totl_min}][sms {cnt_avlb_sms}/{cnt_totl_sms}]\n'
        buff += f'Всего номеров: {cnt_nums}\n'
    except Exception as e:
        return str(e)[:100], {}, ''
    finally:
        if driver: driver.quit()

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
    tlg_mess = ''
    e, data, mess = run_lk_parsing()
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
