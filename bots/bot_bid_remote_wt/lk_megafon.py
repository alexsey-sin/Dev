import time
from datetime import datetime
import requests  # pip install requests
from selenium import webdriver  # $ pip install selenium
from selenium.webdriver.common.by import By


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
        buff += f'balance: {data.get("balance")}\n'
        nums = data.get('numbers')
        cnt_nums = len(nums)
        cnt_avlb_min = 0
        cnt_avlb_sms = 0
        
        for dct in nums:
            str_number = dct.get('number')
            str_avlb_min = dct.get('mobile_available')
            str_avlb_sms = dct.get('sms_available')
            try:
                sub_str = ''
                if str_avlb_min or str_avlb_sms:
                    sub_str += f'{str_number} '
                if str_avlb_min:
                    cnt_avlb_min += int(str_avlb_min)
                    sub_str += f'[min {str_avlb_min}]'
                if str_avlb_sms:
                    cnt_avlb_sms += int(str_avlb_sms)
                    sub_str += f'[sms {str_avlb_sms}]'
                
                if len(sub_str) > 0:
                    buff += sub_str + '\n'
            except:
                continue
        end_time = datetime.now()
        time_str = '\nDuration: {}'.format(end_time - start_time)
        buff += f'Итого: [min {cnt_avlb_min}][sms {cnt_avlb_sms}]\n'
        buff += f'Всего номеров: {cnt_nums}\n'
    except Exception as e:
        return [e, {}, 'error', '']
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
    return [0, data, time_str, buff]


if __name__ == '__main__':
    pass
    rez = run_lk_megafon()
    if rez:
        str_rez = 'Парсинг ЛК Мегафон: ERROR - ' + str(rez)
        print(str_rez)
        # send_telegram(str_rez)
