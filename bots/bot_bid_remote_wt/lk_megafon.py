import time
from datetime import datetime
import requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By

emj_red_mark = '❗️'
emj_red_ball = '🔴'
emj_yellow_ball = '🟡'
emj_green_ball = '🟢'
emj_red_rhomb = '♦️'
emj_yellow_rhomb = '🔸'


def run_lk_megafon():
    start_time = datetime.now()
    ###########################################################################
    ###########################################################################
    # https://b2blk.megafon.ru/login		9201337110	dkk3D2
    driver = None
    try:
        base_url = 'https://b2blk.megafon.ru'
        EXE_PATH = 'driver/chromedriver.exe'
        driver = webdriver.Chrome(executable_path=EXE_PATH)

        driver.implicitly_wait(20)
        driver.get(base_url + '/login')
        time.sleep(3)

        els = driver.find_elements(By.XPATH, '//input[@data-input-login="loginAuthform"]')
        if len(els) != 1: raise Exception(1)
        els[0].send_keys('9201337110')
        time.sleep(1)

        els = driver.find_elements(By.XPATH, '//input[@data-input-pwd="passwordAuthform"]')
        if len(els) != 1: raise Exception(2)
        els[0].send_keys('dkk3D2')
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
        # #===========
        # # time.sleep(10)
        # with open('out_lk.html', 'w', encoding='utf-8') as outfile:
            # outfile.write(driver.page_source)
        # raise Exception('Финиш.')
        # #===========
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
        end_time = datetime.now()
        time_str = '\nDuration: {}'.format(end_time - start_time)
        buff += f'Итого: [min {cnt_avlb_min}][sms {cnt_avlb_sms}]\n'
        buff += f'Всего номеров: {cnt_nums}\n'
    except Exception as e:
        return [str(e)[:100], {}, 'error', '']
    finally:
        if driver: driver.quit()

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
    return ['', data, time_str, buff]

def send_telegram(chat: str, token: str, text: str):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try: requests.post(url, data={'chat_id': chat, 'text': text})
    except: print('ERROR telegram send message.')


if __name__ == '__main__':
    # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    rez = run_lk_megafon()
    if rez:
        str_rez = 'Парсинг ЛК Мегафон: ERROR - ' + str(rez)
        print(str_rez)
        send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, rez[3])
