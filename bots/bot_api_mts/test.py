import os
import time
from datetime import datetime
from datetime import timedelta
import requests  # pip install requests
from dotenv import load_dotenv  # pip install python-dotenv
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import json
from lxml import etree
from xml.dom import minidom


threshold_time_iam_token = timedelta(hours=1)  # живучесть токена

def get_access_token(): # OK
    # Время жизни access_token — не больше 4 часов
    load_dotenv()
    client_id = os.getenv('mts_client_id')
    client_secret = os.getenv('mts_client_secret')
    refresh_token = os.getenv('mts_refresh_token')
    if (client_id == None or len(client_id) == 0
        or client_secret == None or len(client_secret) == 0
        or refresh_token == None or len(refresh_token) == 0):
        print('no secrets')
        return None
    
    iam_bad = False
    token = None
    filename = 'token'
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:  # читаем время создания токена если есть
            js = json.load(file)
        dt_old_str = js.get('time_update')
        dt_old = datetime.strptime(dt_old_str, '%Y-%m-%d %H:%M:%S.%f')
        delta_dt = datetime.now() - dt_old
        if delta_dt > threshold_time_iam_token:
            iam_bad = True
        else:
            token = js.get('access_token')
            print('Token read in file')
    except:
        iam_bad = True

    if iam_bad:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'login.mts.ru',
            'Connection': 'Keep-Alive',
            'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
        }
        data = f'grant_type=refresh_token&client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}'
        url = 'https://login.mts.ru/amserver/oauth2/token'
        try:
            responce = requests.post(url, headers=headers, data=data)
            if responce.status_code != 200: raise
            token = responce.json().get('access_token')
            dict_token = {
                'time_update': str(datetime.now()),
                'access_token': token
            }
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(dict_token, file)
                print('Token download and save')
        except:
            print('error requests or save')
    return token

def get_balance(access_token, number): # OK
    balance = ''
    xml_parser = etree.XMLParser(remove_blank_text=True)
    data_str = f'''
        <soapenv:Envelope xmlns:soapenv='http://schemas.xmlsoap.org/soap/envelope/' xmlns:CustomerManagement='http://www.mts.ru/schema/api/CustomerManagement' xmlns:pag='http://mts.ru/siebel/pagination' xmlns:sec='http://schemas.xmlsoap.org/ws/2002/07/secext' xmlns:sieb='http://mts.ru/siebel' xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
           <soapenv:Header>
              <msisdn>{number}</msisdn>
           </soapenv:Header>
           <soapenv:Body>
              <sieb:GetAccounts>
                 <request>
                    <channel id='NCIH' />
                    <items>
                       <item id='1' xsi:type='CustomerManagement:AccountRequestItem'>
                          <accounts>
                             <account>
                                <balances>
                                   <balance>
                                      <remainedAmount unitOfMeasure='RUB' />
                                   </balance>
                                </balances>
                             </account>
                          </accounts>
                       </item>
                    </items>
                 </request>
              </sieb:GetAccounts>
           </soapenv:Body>
        </soapenv:Envelope>
    '''
    elem_data = etree.XML(data_str, parser=xml_parser)
    data = etree.tostring(elem_data)
    headers = {
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': '',
        'Authorization': f'Bearer {access_token}',
        'Content-Length': f'{len(data)}',
        'Host': 'login.mts.ru:443',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    try:
        url = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/ICustomerManagementService/v1'
        responce = requests.post(url, headers=headers, data=data)
        if responce.status_code != 200: return None
        bs_content = BeautifulSoup(responce.text, 'lxml')
        balance = bs_content.remainedamount['amount']
    except:
        print('error requests or BeautifulSoup parse')
        return None
    return balance

def get_counters(access_token, number): # OK здесь получаем все счетчики по пакетам
    xml_parser = etree.XMLParser(remove_blank_text=True)
    data_str = f'''
        <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
          <s:Header>
            <msisdn>{number}</msisdn>
            <h:SourceCode xmlns="http://mts.ru/siebel" xmlns:h="http://mts.ru/siebel">NCIH</h:SourceCode>
          </s:Header>
          <s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <GetProducts xmlns="http://mts.ru/siebel">
              <request xmlns="">
                <channel id="msisdn"/>
                <items>
                  <item xsi:type="q1:ProductRequestItem" role="" xmlns:q1="http://www.mts.ru/schema/api/ProductManagement">
                    <product>
                      <productOfferings>
                        <productOffering>
                          <categories>
                            <category name="counter"/>
                          </categories>
                        </productOffering>
                      </productOfferings>
                    </product>
                  </item>
                </items>
              </request>
            </GetProducts>
          </s:Body>
        </s:Envelope>
    '''
    elem_data = etree.XML(data_str, parser=xml_parser)
    data = etree.tostring(elem_data)
    headers = {
        'Accept-Encoding': 'gzip,deflate',
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': '',
        'Authorization': f'Bearer {access_token}',
        'Content-Length': f'{len(data)}',
        'Host': 'login.mts.ru:443',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    # try:
    url = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/IProductInventoryService/v1'
    responce = requests.post(url, headers=headers, data=data)
    print(responce.status_code)
    print(responce.text)
    exit()
    # except:
        # return None
    if responce.status_code == 200:
        return responce.text
        
    return None

def get_actual_counters(access_token, number):
    xml_parser = etree.XMLParser(remove_blank_text=True)
    data_str = f'''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:head="http://schemas.sitels.ru/FORIS/IL/Headers" xmlns:nat="http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper">
           <soapenv:Header>
              <head:SubscriberInformation>
                 <head:Login>admsk\esbmsk</head:Login>
                 <head:OperatorType>NCIH_Corporate</head:OperatorType>
              </head:SubscriberInformation>
           </soapenv:Header>
           <soapenv:Body>
              <nat:QueryAccountPhoneInformation>
                 <nat:request>
                    <nat:Accounts xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                    <nat:InfoTypes>
                       <nat:AccountInfoType>Basic</nat:AccountInfoType>
                       <nat:AccountInfoType>CorpBudgetCounters</nat:AccountInfoType>
                    </nat:InfoTypes>
                    <nat:LanguageCode>1</nat:LanguageCode>
                    <nat:Phones>
                       <nat:PhoneId>
                          <nat:Id>{number}</nat:Id>
                       </nat:PhoneId>
                    </nat:Phones>
                 </nat:request>
              </nat:QueryAccountPhoneInformation>
           </soapenv:Body>
        </soapenv:Envelope>
    '''
    elem_data = etree.XML(data_str, parser=xml_parser)
    data = etree.tostring(elem_data)
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': 'http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper/INationalCorporateInternetHelper/QueryAccountPhoneInformation',
        'Authorization': f'Bearer {access_token}',
        'Content-Length': f'{len(data)}',
        'Host': 'login.mts.ru:443',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    # try:
    url = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/NCIH/v1'
    # client = requests.session()
    responce = requests.post(url, headers=headers, data=data)
    if responce.status_code == 200:
        reparsed = minidom.parseString(responce.text)
        resp_str = reparsed.toprettyxml(indent="  ")
        with open('out', 'w', encoding='utf-8') as outfile:
            outfile.write(resp_str)

def get_contracts(access_token): # OK
    url_contracts = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/api/customer/v1/contracts'
    headers = {"Authorization": f"Bearer {access_token}", "Client-type": "curl"}
    responce = requests.get(url_contracts, headers=headers)
    if responce.status_code != 200:
        return None, None
    js_dkt = responce.json()
    return js_dkt.get('contracts').get('contractNumber'), js_dkt.get('inn')

def get_numbers(access_token, contract): # OK
    url_numbers = f'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/api/customer/v1/contracts/{contract}/accounts/phones'
    headers = {"Authorization": f"Bearer {access_token}", "Client-type": "curl"}
    responce = requests.get(url_numbers, headers=headers)
    if responce.status_code != 200:
        return None, None
    js_dkt = responce.json()
    accounts = js_dkt.get('accounts')
    out_dict = {}
    for acc in accounts:
        # print(acc)
        account = acc.get('accountNumber')
        out_lst = []
        phones = acc.get('phones')
        if isinstance(phones, list):
            for ph in phones:
                out_lst.append(ph.get('msisdn'))
        elif isinstance(phones, dict):
            out_lst.append(phones.get('msisdn'))
        out_dict[account] = out_lst
    return out_dict

def get_remains_counters(access_token, number): #  OK Запрос остатка счетчиков КБ по MSISDN:
    # xml_parser = etree.XMLParser(remove_blank_text=True)
    data_str = f'''
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:head="http://schemas.sitels.ru/FORIS/IL/Headers" xmlns:nat="http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper">
           <soapenv:Header>
              <head:SubscriberInformation>
                 <head:Login>admsk\esbmsk</head:Login>
                 <head:OperatorType>NCIH_Corporate</head:OperatorType>
              </head:SubscriberInformation>
           </soapenv:Header>
           <soapenv:Body>
              <nat:QueryAccountPhoneInformation>
                 <nat:request>
                    <nat:Accounts xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                    <nat:InfoTypes>
                       <nat:AccountInfoType>Basic</nat:AccountInfoType>
                       <nat:AccountInfoType>CorpBudgetCounters</nat:AccountInfoType>
                    </nat:InfoTypes>
                    <nat:LanguageCode>1</nat:LanguageCode>
                    <nat:Phones>
                       <nat:PhoneId>
                          <nat:Id>{number}</nat:Id>
                       </nat:PhoneId>
                    </nat:Phones>
                 </nat:request>
              </nat:QueryAccountPhoneInformation>
           </soapenv:Body>
        </soapenv:Envelope>
    '''
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'Client-type': 'curl',
        'SOAPAction': '"http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper/INationalCorporateInternetHelper/QueryAccountPhoneInformation"',
        'Authorization': f'Bearer {access_token}',
        # 'Host': 'login.mts.ru:443',
        # 'Connection': 'Keep-Alive',
        # 'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    url = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/NCIH/v1'
    responce = requests.post(url, headers=headers, data=data_str)
    print(responce.status_code)
    print(responce.text)
    
def proba(token, msisdn): # от мтс

    payload=f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:head="http://schemas.sitels.ru/FORIS/IL/Headers" xmlns:nat="http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper">
       <soapenv:Header>
          <head:SubscriberInformation>
             <head:Login>admsk\esbmsk</head:Login>
             <head:OperatorType>NCIH_Corporate</head:OperatorType>
          </head:SubscriberInformation>
       </soapenv:Header>
       <soapenv:Body>
          <nat:QueryAccountPhoneInformation>
             <nat:request>
                <nat:Accounts xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                <nat:InfoTypes>
                   <nat:AccountInfoType>Basic</nat:AccountInfoType>
                   <nat:AccountInfoType>CorpBudgetCounters</nat:AccountInfoType>
                </nat:InfoTypes>
                <nat:LanguageCode>1</nat:LanguageCode>
                <nat:Phones>
                   <nat:PhoneId>
                      <nat:Id>{msisdn}</nat:Id>
                   </nat:PhoneId>
                </nat:Phones>
             </nat:request>
          </nat:QueryAccountPhoneInformation>
       </soapenv:Body>
    </soapenv:Envelope>"""


    URL="https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/NCIH/v1"
    # msisdn="79992339999"
    # token="токен"
    headers = {"Authorization": f"Bearer {token}"
        , "Client-type": "curl"
        , "Content-Type": "text/xml;charset=UTF-8"
        ,"SOAPAction": "\"http://schemas.sitels.ru/FORIS/IL/NationalCorporateInternetHelper/INationalCorporateInternetHelper/QueryAccountPhoneInformation\""
               }

    resp = requests.post(url=URL, headers=headers, data=payload)
    if resp.status_code == 200:
        print(resp.content)
    else:
        print(resp.status_code)


def main():
    access_token = get_access_token()
    if access_token == None:
        print('No token')
        exit(0)
        
    # contract, inn_client = get_contracts(access_token)
    # if contract == None:
        # print('No contract')
        # exit(0)
        
    # numbers = get_numbers(access_token, contract)
    # for key, val in numbers.items():
        # if key == '276305269415':  # парсим как пакет Умный бизнес M
            # pass
        # elif key == '276305269521':  # парсим как пакет BATC здесь берем только баланс
            # pass
        # elif key == '276305270435':  # парсим как пакет BATC
            # pass
        
        
        
        
        # account = 
        # balance = get_balance(access_token, num)
        # print(num, balance)

# 276305269415 [79109630404, 79109630808, 79109630307, 79109630633, 79109630500, 79109630505, 79109631515, 79109630707]
# 276305269521 [79108100395]
# 276305270435 [79109630112]


    content = get_counters(access_token, '79109630112')
    # sms_packet = sms_available = min_packet = min_available = 0
    # bs_content = BeautifulSoup(content, 'lxml')
    # global_items = bs_content.find_all('item')  # берем все теги item
    # for global_item in global_items:  # берем каждый и копаемся в нем
        # yes_sms = global_item.find(id='UMB500S')
        # if yes_sms:  # Умный бизнес M (смс)
            # productprices = global_item.find_all('productprice')
            # for productprice in productprices:
                # if productprice['name'] == 'PeriodInitialValue':
                    # sms_packet = productprice.find('remainedamount')['amount']
                    # print('sms_packet', sms_packet)
                # if productprice['name'] == 'Counter':
                    # sms_available = productprice.find('remainedamount')['amount']
                    # print('sms_available', sms_available)
            # continue
        # yes_min = global_item.find(id='UMB1100M')
        # if yes_min:  # Умный бизнес M (мин)
            # productprices = global_item.find_all('productprice')
            # for productprice in productprices:
                # if productprice['name'] == 'PeriodInitialValue':
                    # min_packet = productprice.find('remainedamount')['amount']
                    # try:
                        # min_packet = int(float(min_packet) / 60)
                    # except:
                        # min_packet = 0
                    # print('min_packet', min_packet)
                # if productprice['name'] == 'Counter':
                    # min_available = productprice.find('remainedamount')['amount']
                    # try:
                        # min_available = int(float(min_available) / 60)
                    # except:
                        # min_available = 0
                    # print('min_available', min_available)
            # break
            
    buff = ''
    sms_packet = sms_available = min_packet = min_available = 0
    bs_content = BeautifulSoup(content, 'lxml')
    global_items = bs_content.find_all('item')  # берем все теги item
    for global_item in global_items:  # берем каждый и копаемся в нем
        yes_min = global_item.find(id='ATCM500')
        if yes_min:  # ВАТС M (мин)
            print('yes_min')
            productprices = global_item.find_all('productprice')
            for productprice in productprices:
                if productprice['name'] == 'PeriodInitialValue':
                    min_packet = productprice.find('remainedamount')['amount']
                    try:
                        min_packet = int(float(min_packet) / 60)
                    except:
                        min_packet = 0
                if productprice['name'] == 'Counter':
                    min_available = productprice.find('remainedamount')['amount']
                    try:
                        min_available = int(float(min_available) / 60)
                    except:
                        min_available = 0
            break
    # ==== конец парсинга
    # ==== формируем отчет
    if min_available or min_packet:
        buff += f'  [min {min_available}/{min_packet}]'

    print(buff)
    # balance = bs_content.remainedamount['amount']

    # если надо слить в файл
    # reparsed = minidom.parseString(content)
    # resp_str = reparsed.toprettyxml(indent="  ")
    # with open('out', 'w', encoding='utf-8') as outfile:
        # outfile.write(resp_str)
    
    
    
    
    
    
    
    
    
    
    
    
        # if responce.status_code == 200:
        # reparsed = minidom.parseString(responce.text)
        # resp_str = reparsed.toprettyxml(indent="  ")
        # with open('out', 'w', encoding='utf-8') as outfile:
            # outfile.write(responce.text)
    # elem_data = etree.XML(data_str, parser=xml_parser)
    # data = etree.tostring(elem_data)
    # # try:
    # # client = requests.session()



    
    
    
    
    
    
    
    # get_remains_counters(access_token, '79109630404')

    
    # balance = get_balance(access_token, '79109630808')  # 1767.3
    # balance = get_balance(access_token, '79109630404')  # 1767.3
    # balance = get_balance(access_token, '79109630112')  # 1080.0
    # balance = get_balance(access_token, '79108100395')  # 0.0
    
    
    
    # print(balance)
    
    
    # contracts
    # counters
    # get_actual_counters(access_token, '79109630404')
    # get_actual_counters(access_token, '79109630112')

if __name__ == '__main__':
    main()

    # rez = main()
    # if rez:
        # str_rez = 'Парсинг ЛК МТС: ERROR - ' + str(rez)
        # print(str_rez)
        # send_telegram(str_rez)






# obj = soup.find(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['photo'])
# meme_links[:3]






# +7 910 963 0633     276305269415                      Лицевой счёт:  276305269415
# +7 910 963 0307     276305269415
# +7 910 963 0404     276305269415  основной
# +7 910 963 0808     276305269415                      Тарифный план Умный бизнес безлимит  1000 шт
# +7 910 963 1515     276305269415                      1 767,30 ₽
# +7 910 963 0505     276305269415          
# +7 910 963 0500     276305269415
# +7 910 963 0707     276305269415

# +7 910 810 0395     276305269521                      0,00 ₽                          Лицевой счёт:   276305269521
# +7 910 963 0112     276305270435                      1 080,00 ₽  ВАТС M   491 мин    Лицевой счёт:   276305270435

# Контракт:    ООО «Домконнект» 176305178278



