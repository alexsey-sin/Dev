import os
from datetime import datetime
from datetime import timedelta
from dotenv import load_dotenv  # pip install python-dotenv
import requests  # pip install requests

threshold_time_iam_token = timedelta(hours=1)  # живучесть токена

def get_access_token():
    # Время жизни access_token — не больше 4 часов
    load_dotenv()
    client_id = os.getenv('mts_client_id')
    client_secret = os.getenv('mts_client_secret')
    refresh_token = os.getenv('mts_refresh_token')
    if len(client_id) == 0 or len(client_secret) == 0 or len(refresh_token) == 0:
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
        print(responce.text)
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
    access_token = get_access_token()
    
    num_s = [
        '79109630633',
        '79109630307',
        '79109630404',
        '79109630808',
        '79109631515',
        '79109630505',
        '79109630500',
        '79109630707',

        '79108100395',
        '79109630112',
    ]
    buf = ''
    for num in num_s:
        balance = get_balance(access_token, num)
        buff += f'Balance {num}: {balance}\n'
    ###################### Всем спасибо, все свободны ######################
    return [0, {}, '', buff]


if __name__ == '__main__':
    pass
    
    # Личный кабинет
    # https://lk-b2b.mts.ru
    # 79109630404
    # !3W^f-QN

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