import os
import time
from datetime import datetime
import requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By
import json

# from datetime import timedelta
# from dotenv import load_dotenv
# from bs4 import BeautifulSoup  # pip install beautifulsoup4
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.common.by import By
# import sys


TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'


def send_telegram(text: str):
    url = "https://api.telegram.org/bot" + TELEGRAM_TOKEN + "/sendMessage"

    r = requests.post(url, data={
         "chat_id": TELEGRAM_CHAT_ID,
         "text": text
          })

def main() -> int:
    start_time = datetime.now()
    ###########################################################################
    ###########################################################################
    # https://lk-b2b.mts.ru		79109630404	!3W^f-QN


    base_url = 'https://lk-b2b.mts.ru'
    login = '9109630404'
    password = '!3W^f-QN'

    # EXE_PATH = r'c:/Dev/parsing_Megafon/driver/chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=EXE_PATH)

    EXE_PATH = r'c:/Dev/parsing_MTS/driver/firefoxdriver.exe'
    driver = webdriver.Firefox(executable_path=EXE_PATH)

    driver.implicitly_wait(20)
    driver.get(base_url)

    ###################### Страница логина ######################
    time.sleep(2)
    cnt = 0
    while True:
        try:
            el_input = driver.find_element(By.XPATH, '//input[@id="phoneInput"]')
            el_button = driver.find_element(By.XPATH, '//button[@id="submit"]')

            el_input.send_keys(login)
            el_button.click()
            break
        except:
            time.sleep(1)
        
        cnt += 1
        if cnt > 5: driver.quit(); return 1
    ###################### Страница пароля ######################
    time.sleep(2)  # чтобы успела загрузиться страница и отработать скрипты
    cnt = 0
    while True:
        try:
            el_input = driver.find_element(By.XPATH, '//input[@id="password"]')
            el_button = driver.find_element(By.XPATH, '//button[@id="submit"]')

            el_input.send_keys(password)
            el_button.click()
            break
        except:
            time.sleep(1)

        cnt += 1
        if cnt > 5: driver.quit(); return 2
    ###################### Главная страница ######################
    time.sleep(2)
    cnt = 0
    while True:
        try:
            el_number = driver.find_element(By.XPATH, '//a[@data-key="homePage.operationsPage"]')
            el_number.click()
            break
        except:
            time.sleep(1)

        cnt += 1
        if cnt > 5: driver.quit(); return 2
    ###################### Страница номеров ######################
    time.sleep(5)

    els_row_num = driver.find_elements(by=By.CSS_SELECTOR, value='div.columns.columns--thickness-base.ng-star-inserted')
    if len(els_row_num) == 0: driver.quit(); return 3
    driver.implicitly_wait(0)
    
    dkt_num = {}
    for el_row_num in els_row_num:
        els_num = el_row_num.find_elements(By.XPATH, './/a[@data-ii="billingHierarchy.phoneNumberLink"]')
        if len(els_num) != 1: continue
        str_num = els_num[0].text.strip()
        str_num = str_num.replace(' ', '').replace('+', '')
        els_acc = el_row_num.find_elements(By.XPATH, './/a[@data-ii="billingHierarchy.accountNumberLink"]')
        if len(els_acc) != 1: driver.quit(); return 4  # если в строке нашелся номер - должен быть и счет
        str_acc = els_acc[0].text.strip()
        dkt_num[str_num] = str_acc

    ###################### Страницы каждого номера ######################
    dct_cookie = {}
    for num, acc in dkt_num.items():
        url = f'https://lk-b2b.mts.ru/ncih_new/billing/flow/select(overlay:card/td;td={num};pa={acc};contract=176305178278)'
        driver.get(url)
        driver.implicitly_wait(20)
        time.sleep(3)

        els_block = driver.find_elements(By.XPATH, '//card-td-operations[@data-key="cardTD.operations"]')
        if len(els_block) != 1:  driver.quit(); return 5
        
        els_icon = els_block[0].find_elements(By.XPATH, './/c-icon[@data-key="cardTD.makeTransitionToIHelper"]')
        if len(els_icon) != 1:  driver.quit(); return 6
        els_icon[0].click()
        
        ###################### Личный кабинет каждого номера ######################
        time.sleep(20)

        try:
            cookie = driver.get_cookie('MTSWebSSO')
        except:
            driver.quit(); return 7
        
        headers_post = {
            'Content-Type': 'application/json',
            'Cookie': f'MTSWebSSO={cookie}',
            'Authorization': 'Bearer 35734616-e607-3451-b838-a564b7f66c8e',
            'Host': 'login.mts.ru:443',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        }
        data_post = {
            "client_owner": "domconnect",
            "email": "adm.tt76@gmail.com",
        }
        url_post = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/WebSSORegistration/v1'
        
        response = requests.post(url_post, headers=headers_post, data=data_post)
        if response.status_code == 201:
            dct_cookie[num] = response.json()
        else:
            dct_cookie[num] = None
            print(num, 'get key oauth', response.status_code)
            print(response.json())

        break
    
    with open('oauth_mts_api.json', 'w', encoding='utf-8') as file:
        json.dump(dct_cookie, file)

    # POST https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/WebSSORegistration/v1
    # Content-Type: application/json
    # Cookie: MTSWebSSO=cookie взятые из личного кабинета
    # Authorization: Bearer 35734616-e607-3451-b838-a564b7f66c8e
    # Host: login.mts.ru:443
    # Connection: Keep-Alive
    # User-Agent: Apache-HttpClient/4.1.1 (java 1.5)
    # { 
    # "client_owner":"owner name", 
    # "email":"email"
    # }

    # buff = ''
    # for num, val in dct_cookie.items():
    #     buff += f'num: {num}\n'
    #     buff += f'    MTSWebSSO: {val}\n'

    # with open('num_cookie.txt', 'w', encoding='utf-8') as outfile:
    #     outfile.write(buff)
    
    #     headers = {
    #     'Authorization': f'Bearer {iam_token}',
    # }
    # data = {
    #     'lang': 'ru-RU',
    #     'folderId': f'{Y_ID_FOLDER}',
    #     'text': f'{my_text}'
    # }

    # response = requests.post(Y_TTS_URL, headers=headers, data=data)

    
    
    

    # with open('out_file.html', 'w', encoding='utf-8') as outfile:
    #     outfile.write(driver.page_source)
    
    # print(f'num: <{str_num}>; acc: <{str_acc}>')
    # url = 'https://lk-b2b.mts.ru/ncih_new/billing/flow/select(overlay:card/td;td=79109630633;pa=276305269415;contract=176305178278)'
    # driver.get(url)
    
    # time.sleep(10)
    
    
    # url = 'https://lk-b2b.mts.ru/ncih_new/billing/flow/select(overlay:card/td;td=79109630404;pa=276305269415;contract=176305178278)'
    # driver.get(url)
    
    # time.sleep(10)
    # els = driver.find_elements(By.XPATH, '//a[@data-key="homePage.operationsPage"]')
    # if len(els) != 1: driver.quit(); return 1
    # els[0].send_keys('9201337110')

    # els = driver.find_elements(By.XPATH, '//input[@data-input-pwd="passwordAuthform"]')
    # if len(els) != 1: driver.quit(); return 2
    # els[0].send_keys('dkk3D2')
    
    # els = driver.find_elements(By.XPATH, '//button[@data-button="buttonSubmitAuthform"]')
    # if len(els) != 1: driver.quit(); return 3
    # els[0].click()


    ###################### Главная страница ######################
    # els = driver.find_elements(By.CLASS_NAME, 'widget-personal-account__current-balance')
    # if len(els) != 1: driver.quit(); return 4
    # els1 = els[0].find_elements(By.CLASS_NAME, 'widget-personal-account__balance-text')
    # if len(els1) != 1: driver.quit(); return 5

    # data = {
    #     'operator': 'megafon',
    #     'balance': els1[0].text.strip(),
    #     'numbers': [],
    # }

    # # переходим на страницу абоненты
    # driver.get(base_url + '/subscribers/mobile')

    ###################### Абоненты ######################
    # need_rows = 18  # (кол-во номеров + строка заголовка)
    # cnt = 0
    # while(1):
    #     els = driver.find_elements(By.XPATH, '//div[@data-col-name="msisdn"]')
    #     if len(els) >= need_rows:
    #         break
    #     else:
    #         time.sleep(1)
    #     if cnt > 25: driver.quit(); return 6
    #     cnt += 1
    
    # dct_nums = {}
    # for i in range(1, len(els)):
    #     el = els[i].find_elements(By.TAG_NAME, 'a')
    #     if len(el) != 1: driver.quit(); return 7
    #     dct_nums[el[0].text] = el[0].get_attribute('href')

    ###################### Перебираем страницы абонентов ######################
    # for key, value in dct_nums.items():
    #     driver.get(value)  # value = типа: https://b2blk.megafon.ru/subscriber/info/124701207
    #     driver.implicitly_wait(2)
    #     time.sleep(3)

    #     number = {'number': key, }

    #     els = driver.find_elements(By.XPATH, '//div[@id="discountsList"]')
    #     if len(els) != 1: driver.quit(); return 9
    #     els_dl = els[0].find_elements(By.TAG_NAME, 'dl')
    #     if len(els_dl) == 0:
    #         data['numbers'].append(number)  
    #         continue

    #     for el_dl in els_dl:  # по блокам <dl>
    #         dts = el_dl.find_elements(By.TAG_NAME, 'dt')
    #         if len(dts) != 1: driver.quit(); return 10
    #         label = dts[0].text
            
    #         if label.find('SMS') >= 0:  # блок с 'SMS'
    #             divs = el_dl.find_elements(By.TAG_NAME, 'div')
    #             for div in divs:
    #                 dat = div.text
    #                 if dat.find('доступно') >= 0:
    #                     available = dat.split()[1]
    #                     number['sms_available'] = available

    #         elif label.find('Минут') >= 0:  # блок с 'Минут'
    #             divs = el_dl.find_elements(By.TAG_NAME, 'div')
    #             for div in divs:
    #                 dat = div.text
    #                 if dat.find('доступно') >= 0:
    #                     available = dat.split()[1]
    #                     number['mobile_available'] = available

    #     data['numbers'].append(number)

    ###################### Вывод ######################
    # row = f'{data.get("operator")} balance: {data.get("balance")}'
    # buff = row + '\n'
    # print(row)
    # for dct in data.get('numbers'):
    #     my_str = dct.get('number', None)
    #     if my_str:
    #         row = '    ' + my_str
    #         buff += row + '\n'
    #         print(row)
    #     my_str = dct.get('mobile_available', None)
    #     if my_str:
    #         row = '        mobile_available: ' + my_str
    #         buff += row + '\n'
    #         print(row)
    #     my_str = dct.get('sms_available', None)
    #     if my_str:
    #         row = '        sms_available: ' + my_str
    #         buff += row + '\n'
    #         print(row)
    ###################### Формируем POST запрос в базу данных ######################
    '''
    структура отправляемых данных:
    data = {
        'operator': 'beeline',
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
    # responce = requests.post('https://httpbin.org/post', data=data)
    # if responce.status_code != 200: driver.quit(); return responce.status_code
    
    # end_time = datetime.now()
    # time_str = '\nDuration: {}'.format(end_time - start_time)
    # buff += time_str + '\n'
    # print(time_str)
    # ###################### Формируем log ######################
    # if not os.path.exists('log/'):
    #     os.mkdir('log/')

    # now = datetime.now()
    # filename = now.strftime('log/log_%H-%M_%d-%m-%Y.txt')

    # with open(filename, 'w', encoding='utf-8') as outfile:
    #     outfile.write(buff)

    # with open('out_file.html', 'w', encoding='utf-8') as outfile:
    #     outfile.write(driver.page_source)

    ###################### Всем спасибо, все свободны ######################
    driver.quit()
    return 0


if __name__ == '__main__':
    rez = main()
    if rez:
        str_rez = 'Парсинг ЛК МТС: ERROR - ' + str(rez)
        print(str_rez)
        # send_telegram(str_rez)

# хорошая статья про BeautifulSoup: https://habr.com/ru/company/ods/blog/346632/

# obj = soup.find(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links[:3]

