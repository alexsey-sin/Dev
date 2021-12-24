# from selenium import webdriver  # $ pip install selenium
# from selenium.webdriver.common.by import By
    # set_did()
    
    
    # set_bid_domru_status()
    # go_domru()
    # analiz()
    # selenium()
    # get_street()
    
    
    # send_test_zayavka()
    
    
    
    # https://dealers.dom.ru/request/widget/assets/6ad915b2/yii.activeForm.js
    # https://dealers.dom.ru/request/widget?domain=yar&amp;referral_id=1000096145
    
            # if responce.status_code != 200: raise
        # token = responce.json().get('access_token')
        # dict_token = {
            # 'time_update': str(datetime.now()),
            # 'access_token': token
        # }
        # with open(filename, 'w', encoding='utf-8') as file:
            # json.dump(dict_token, file)
    # except Exception as e:
        # print(e)
            # print(responce.status_code)
        # with open('crm.html', 'w', encoding='utf-8') as f:
            # f.write(responce.text)

    # pass


# def send_test_zayavka():
    # user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # headers = {
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    # }
    # session = requests.Session()
    # url = 'https://dealers.dom.ru/'
    
    # params = {
        # 'domain': 'yar',
        # 'referral_id': '1000096145',
    # }

    # url += 'request/widget'
    # resp = session.get(url, headers=headers, params=params)
    # session.headers.update({'Referer':url})
    # session.headers.update({'User-Agent':user_agent_val})
    
    # bs_content = BeautifulSoup(resp.text, 'html.parser')
    
    # el_csrf = bs_content.find('meta', attrs={'name': 'csrf-token'})
    # csrf = el_csrf['content']  # print(csrf)
    
    # form = {
        # '_csrf': csrf,
        # 'WidgetForm[referralId]': '1000096145',
        # 'WidgetForm[city]': 'volgograd',
        # 'WidgetForm[street]': 'пр-т ленина',
        # 'WidgetForm[streetId]': '1',
        # 'WidgetForm[house]': '13',
        # 'WidgetForm[houseId]': '1',
        # 'WidgetForm[flat]': '22',
        # 'WidgetForm[name]': 'Игорь',
        # 'WidgetForm[phone]': '+7 111 111-11-11',
        # 'WidgetForm[email]': '',
        # 'WidgetForm[prim]': 'Тестовая заявка, просьба не обрабатывать.',
        # 'WidgetForm[internet]': 1,
        # 'WidgetForm[tv]': 0,
        # 'WidgetForm[telephony]': 0,
    # }
    # resp = session.post(url, headers=headers, params=params, data=form)

    # print(resp.status_code)
    # print(resp.text)
   
    # with open('answer.html', 'w', encoding='utf-8') as f:
        # f.write(resp.text)
    # # Заявка отправлена!!!
    # pass




# def analiz():
    # with open('zayavka.html', 'r', encoding='utf-8') as f:
        # content = f.read()
    # bs_content = BeautifulSoup(content, 'html.parser')
    
    # el_csrf = bs_content.find('meta', attrs={'name': 'csrf-token'})
    # csrf = el_csrf['content']  # print(csrf)
  
    # # els_city = bs_content.find_all('option')
    # # for el_city in els_city:
        # # print(el_city['value'], el_city.text)
    
    # els_input = bs_content.find_all('input')
    # s_str = ''
    # for el_input in els_input:
        # # print(el_input['name'], el_input.text)
        # s_str += str(el_input) + '\n\n\n'
        # # print(el_input)
    # with open('inputs.html', 'w', encoding='utf-8') as f:
        # f.write(s_str)


# def selenium():
    # base_url = 'https://dealers.dom.ru/request/widget?domain=yar&amp;referral_id=1000096145'
    
    # EXE_PATH = r'c:/Dev/domru/driver/chromedriver.exe'
    # driver = webdriver.Chrome(executable_path=EXE_PATH)

    # # EXE_PATH = r'c:/Dev/bot_opsos/driver/firefoxdriver.exe'
    # # driver = webdriver.Firefox(executable_path=EXE_PATH)

    # driver.implicitly_wait(20)
    # driver.get(base_url)
    # time.sleep(5)
    # with open('out_file.html', 'w', encoding='utf-8') as outfile:
        # outfile.write(driver.page_source)
    # driver.quit()

   
# def go_domru():
    # user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    # # headers = {
        # # 'Content-Type': 'application/x-www-form-urlencoded',
        # # 'Connection': 'Keep-Alive',
        # # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    # # }
    # # params = {
        # # 'key': 'Q8kGM1HfWz',
    # # }
    # session = requests.Session()
    # url = 'https://dealers.dom.ru/'
    # # resp = session.get(url, headers = {'User-Agent': user_agent_val})
    # # session.headers.update({'Referer':url})
    # # session.headers.update({'User-Agent':user_agent_val})
    
    # # payload = {
        # # 'login': 'inetyar.boss@gmail.com',
        # # 'password': 'cGzw8Z4f'
    # # }
    # # resp = session.post(url, data=payload)
    # # if resp.status_code != 200:
        # # print('status_code', resp.status_code, 'Ошибка входа')
        # # return
    
    # params = {
        # 'domain': 'yar',
        # 'referral_id': '1000096145',
    # }
    # # https://dealers.dom.ru/request/widget?domain=yar&referral_id=1000096145
    # url += 'request/widget'
    # resp = session.get(url, params=params)
    # session.headers.update({'Referer':url})
    # session.headers.update({'User-Agent':user_agent_val})
    # # resp = session.post(url)
   
    # print(resp.status_code)
    # with open('hh_success.html', 'w', encoding='utf-8') as f:
        # f.write(resp.text)


# def set_did():
    # # url = 'http://127.0.0.1:8000/api/set_bid_domru'
    # url = 'http://django.domconnect.ru/api/set_bid_domru'
    
    # headers = {
        # 'Content-Type': 'application/x-www-form-urlencoded',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    # }
    # params = {
        # 'key': 'Q8kGM1HfWz',
        # 'city': 'Воронеж',
        # 'street': 'пр-т Октября',
        # 'house': '13а',
        # 'apartment': '25',
        # 'name': 'Василий',
        # 'phone': '79019993656',
        # 'service_tv': 0,
        # 'service_net': 1,
        # 'service_phone': 0,
        # 'comment': 'test',
    # }
    
    # try:
        # responce = requests.get(url, headers=headers, params=params)
    # except:
        # pass
    # print(responce.status_code)
    # # print(responce.text)
    
    # with open('ddd.html', 'w', encoding='utf-8') as f:
        # f.write(responce.text)


