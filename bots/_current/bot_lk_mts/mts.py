import os
from datetime import datetime
from datetime import timedelta
import time
from dotenv import load_dotenv  # pip install python-dotenv
import requests  # pip install requests
from lxml import etree
from bs4 import BeautifulSoup  # pip install beautifulsoup4
import json

threshold_time_iam_token = timedelta(hours=1)  # живучесть токена

def get_access_token(new_token):
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

    if iam_bad or new_token:
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
        except Exception as e:
            print(e)
    return token

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
        account = str(acc.get('accountNumber'))
        out_lst = []
        phones = acc.get('phones')
        if isinstance(phones, list):
            for ph in phones:
                out_lst.append(str(ph.get('msisdn')))
        elif isinstance(phones, dict):
            out_lst.append(str(phones.get('msisdn')))
        out_dict[account] = out_lst
    return out_dict

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
    try:
        url = 'https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/IProductInventoryService/v1'
        responce = requests.post(url, headers=headers, data=data)
    except:
        return None
    if responce.status_code == 200:
        return responce.text
        
    return None

def get_balance(access_token, number):
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

def run_mts():
    ###########################################################################
    ###########################################################################
    print('run_mts')
    cnt_error = 0
    new_token = False
    while True:
        if cnt_error > 3:
            return [1, {}, '', 'No contract or no access']
        
        access_token = get_access_token(new_token)
        if access_token == None:
            return [1, {}, '', 'No access_token']
        
        time.sleep(2)
        contract, inn_client = get_contracts(access_token)
        if contract == None:
            new_token = True
            time.sleep(2)
            cnt_error += 1
            continue
        else:
            break
    
    time.sleep(2)    
    numbers = get_numbers(access_token, contract)
    out_dict = {
        'operator': 'mts',
        'numbers': [],
    }
    buff = 'MTS Balances:\n'
    for key, val in numbers.items():
        if key == '276305269415':  # парсим как пакет Умный бизнес M
            cnt_avlb_min = 0
            cnt_totl_min = 0
            cnt_avlb_sms = 0
            cnt_totl_sms = 0
            for num in val:
                time.sleep(2)
                balance = get_balance(access_token, num)
                buff += f'{num}: {balance}p.\n'
                number = {'number': num, 'balance': balance}
                # ==== парсим Умный бизнес M
                time.sleep(2)
                content = get_counters(access_token, num)
                if content == None:
                    buff += '   get_counters - None\n'
                    continue
                sms_packet = sms_available = min_packet = min_available = 0
                bs_content = BeautifulSoup(content, 'lxml')
                global_items = bs_content.find_all('item')  # берем все теги item
                for global_item in global_items:  # берем каждый и копаемся в нем
                    yes_sms = global_item.find(id='UMB500S')
                    if yes_sms:  # Умный бизнес M (смс)
                        productprices = global_item.find_all('productprice')
                        for productprice in productprices:
                            if productprice['name'] == 'PeriodInitialValue':
                                try:
                                    sms_packet = int(productprice.find('remainedamount')['amount'])
                                    number['sms_total'] = sms_packet
                                except:
                                    sms_packet = 0
                            if productprice['name'] == 'Counter':
                                try:
                                    sms_available = int(productprice.find('remainedamount')['amount'])
                                    number['sms_available'] = sms_available
                                except:
                                    sms_available = 0
                        continue
                    yes_min = global_item.find(id='UMB1100M')
                    if yes_min:  # Умный бизнес M (мин)
                        productprices = global_item.find_all('productprice')
                        for productprice in productprices:
                            if productprice['name'] == 'PeriodInitialValue':
                                min_packet = productprice.find('remainedamount')['amount']
                                try:
                                    min_packet = int(float(min_packet) / 60)
                                    number['mobile_total'] = min_packet
                                except:
                                    min_packet = 0
                            if productprice['name'] == 'Counter':
                                min_available = productprice.find('remainedamount')['amount']
                                try:
                                    min_available = int(float(min_available) / 60)
                                    number['mobile_available'] = min_available
                                except:
                                    min_available = 0
                        break
                out_dict['numbers'].append(number)
                # ==== конец парсинга
                # ==== формируем отчет
                sub_str = ''
                if min_available or min_packet or sms_available or sms_packet:
                    sub_str += '  '
                if min_available:
                    cnt_avlb_min += min_available
                if min_packet:
                    cnt_totl_min += min_packet
                if min_available or min_packet:
                    sub_str += f'[min {min_available}/{min_packet}]'
                if sms_available:
                    cnt_avlb_sms += sms_available
                if sms_packet:
                    cnt_totl_sms += sms_packet
                if sms_available or sms_packet:
                    sub_str += f'[sms {sms_available}/{sms_packet}]'
                
                if len(sub_str) > 0:
                    buff += sub_str + '\n'
            buff += f'Итого: [min {cnt_avlb_min}/{cnt_totl_min}][sms {cnt_avlb_sms}/{cnt_totl_sms}]\n\n'
            # ==== формируем словарь для api
            # ==== конец 
        elif key == '276305269521':  # парсим как пакет BATC здесь берем только баланс
            for num in val:
                time.sleep(2)
                balance = get_balance(access_token, num)
                buff += f'{num}: {balance}p.\n'
                number = {'number': num, 'balance': balance}
                
                out_dict['numbers'].append(number)
                
        elif key == '276305270435':  # парсим как пакет BATC
            for num in val:
                time.sleep(2)
                balance = get_balance(access_token, num)
                buff += f'{num}: {balance}p.\n'
                number = {'number': num, 'balance': balance}

                # ==== парсим ВАТС M
                time.sleep(2)
                content = get_counters(access_token, num)
                if content == None:
                    buff += '   get_counters - None\n'
                    continue
                sms_packet = sms_available = min_packet = min_available = 0
                bs_content = BeautifulSoup(content, 'lxml')
                global_items = bs_content.find_all('item')  # берем все теги item
                for global_item in global_items:  # берем каждый и копаемся в нем
                    yes_min = global_item.find(id='ATCM500')
                    if yes_min:  # ВАТС M (мин)
                        productprices = global_item.find_all('productprice')
                        for productprice in productprices:
                            if productprice['name'] == 'PeriodInitialValue':
                                min_packet = productprice.find('remainedamount')['amount']
                                try:
                                    min_packet = int(float(min_packet) / 60)
                                    number['mobile_total'] = min_packet
                                except:
                                    min_packet = 0
                            if productprice['name'] == 'Counter':
                                min_available = productprice.find('remainedamount')['amount']
                                try:
                                    min_available = int(float(min_available) / 60)
                                    number['mobile_available'] = min_available
                                except:
                                    min_available = 0
                        break
                # ==== конец парсинга
                # ==== формируем отчет
                if min_available or min_packet:
                    buff += f'  [min {min_available}/{min_packet}]'
                
                out_dict['numbers'].append(number)
            # ==== формируем словарь для api
            # ==== конец 
    ###################### Всем спасибо, все свободны ######################
    return [0, out_dict, '', buff]


if __name__ == '__main__':
    pass


# 79109630633
# 79109630307
# 79109630404
# 79109630808
# 79109631515
# 79109630505
# 79109630500
# 79109630707

# 79108100395
# 79109630112
    '''
    структура отправляемых данных:
    data = {
        'operator': 'mts',
        'numbers': [
            {
                'number': '+7(961)161-25-00',
                'balance': '-23.25',
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
