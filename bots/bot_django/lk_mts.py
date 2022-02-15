import requests, json, time


def get_token():  # Получение токена по логину и паролю
    login = 'YrxF9TvrPlK6fbkJNBilUqCw0vUa'
    password = 'hFtsFhai1ZjtuYg_y58fArkaBCEa'
    url = 'https://api.mts.ru/token'

    mess = ''
    token = ''
    auth = (login, password)
    data = {'grant_type': 'client_credentials'}

    try:
        resp = requests.post(url, auth=auth, data=data, timeout=3)
        if resp.status_code == 200:
            dct_answer = json.loads(resp.text)
            token = dct_answer.get('access_token')
            expires_in = dct_answer.get('expires_in')
            print(expires_in)
            if not token:
                fault = dct_answer.get('fault')
                if fault: mess = f'ERROR: {fault.get("message")} {fault.get("description")}'
        else: mess = f'ERROR get_token: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_token: try/except: {e}'
    return mess, token

def get_balance(token, msisdn):  # Получение баланса по номеру MSISDN (7...)
    url = 'https://api.mts.ru/b2b/v1/Bills/CheckBalanceByMSISDN'
    mess = ''
    amount = None
    headers = {
        'ChannelId': 'NCIH_National_PAPI',
        'Authorization': f'Bearer {token}',
    }
    params = {'characteristic.value': msisdn}

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=3)
        if resp.status_code == 200:
            lst_answer = json.loads(resp.text)
            if type(lst_answer) == list and len(lst_answer) > 0: dct_answer = lst_answer[0]
            else: raise Exception('Invalid answer 1')
            lst_cuAccBal = dct_answer.get('customerAccountBalance')
            if not lst_cuAccBal or type(lst_cuAccBal) != list: raise Exception('Invalid answer 2')
            dct_cuAccBal = lst_cuAccBal[0]
            if type(dct_cuAccBal) != dict: raise Exception('Invalid answer 3')
            dct_rmAmount = dct_cuAccBal.get('remainedAmount')
            if type(dct_rmAmount) != dict: raise Exception('Invalid answer 4')
            amount = dct_rmAmount.get('amount')
            if not amount: raise Exception('Invalid answer 5')
        else: mess = f'ERROR get_balance: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_balance: try/except: {e}'
    return mess, amount

def get_validity_info(token, msisdn):  # Получение баланса по номеру MSISDN (7...)
    url = 'https://api.mts.ru/b2b/v1/Bills/ValidityInfo'
    mess = ''
    amount = None
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'ChannelId': 'NCIH_National_PAPI',
        'Authorization': f'Bearer {token}',
    }
    params = {
        'customerAccount.accountNo': msisdn,
        'customerAccount.productRelationship.product.productLine.name': 'Counters',
    }

    try:
        resp = requests.get(url, headers=headers, params=params, data={}, timeout=10)
        if resp.status_code == 200:
            lst_answer = json.loads(resp.text)
            with open('validity_info.json', 'w', encoding='utf-8') as out_file:
                json.dump(lst_answer, out_file, ensure_ascii=False, indent=4)
            print('Ok')
            # print(json.dumps(lst_answer, indent=2))
            # if type(lst_answer) == list and len(lst_answer) > 0: dct_answer = lst_answer[0]
            # else: raise Exception('Invalid answer 1')
            # lst_cuAccBal = dct_answer.get('customerAccountBalance')
            # if not lst_cuAccBal or type(lst_cuAccBal) != list: raise Exception('Invalid answer 2')
            # dct_cuAccBal = lst_cuAccBal[0]
            # if type(dct_cuAccBal) != dict: raise Exception('Invalid answer 3')
            # dct_rmAmount = dct_cuAccBal.get('remainedAmount')
            # if type(dct_rmAmount) != dict: raise Exception('Invalid answer 4')
            # amount = dct_rmAmount.get('amount')
            # if not amount: raise Exception('Invalid answer 5')
        else: mess = f'ERROR get_validity_info: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_validity_info: try/except: {e}'
    return mess, amount



def run(log):
    # log = logging.getLogger(__name__)
    log.debug('lk_mts:  run')
    # pass

if __name__ == '__main__':
    '''
        Ограничения тарифа "Бесплатно"
        до 60 вызовов в минуту
        до 3 вызовов в секунду

    '''
    m, token = get_token()
    if m: print(m); exit()
    print(token)
    time.sleep(1.5)

    # m, balance = get_balance(token, '79109630505')
    # if m: print(m); exit()
    # print(balance)
    # time.sleep(1.5)

    m, balance = get_validity_info(token, '79109630505')
    # m, balance = get_validity_info(token, '79109630112')
    if m: print(m); exit()




'''
    Личный кабинет
    https://lk-b2b.mts.ru
    79109630404
    !3W^f-QN

    Получение токена
    LOGIN:      YrxF9TvrPlK6fbkJNBilUqCw0vUa
    PASSWORD:   hFtsFhai1ZjtuYg_y58fArkaBCEa

    Инфо о балансе по номеру стр. 7
    Инфо о балансе по лицевому счету стр. 9
    Детализация за период по номеру стр. 12
    Детализация за период по лицевому счету стр. 14
    Детализация за период по номеру (расширенная) стр. 15
    Детализация за период по лицевому счету (расширенная) стр. 19
    Запрос остатков минут, интернет, СМС стр. 20


    MTS Balances:
    79109630404: 89.4p.
    [min 45/1400]
    79109630808: 89.4p.
    [min 0/1400]
    79109630307: 89.4p.
    [min 0/1400]
    79109630633: 89.4p.
    [min 35/1400]
    79109630500: 89.4p.
    79109630505: 89.4p.
    79109631515: 89.4p.
    79109630707: 89.4p.
    76850047000: 89.4p.
    Итого: [min 80/5600][sms 0/0]

    79108100395: 0.0p.
    79109630112: -990.0p.
    [min 500/500]

Получение токена
curl --request POST "https://api.mts.ru/token" -u "YrxF9TvrPlK6fbkJNBilUqCw0vUa:hFtsFhai1ZjtuYg_y58fArkaBCEa" -d "grant_type=client_credentials"

Запрос остатков минут, интернет, СМС
curl --location --request GET 'https://api.mts.ru/b2b/v1/Bills/ValidityInfo?customerAccount.accountNo=79109630505&customerAccount.productRelationship.product.productLine.name=Counters' \
--header 'ChannelId:NCIH_National_PAPI'\
--header 'Authorization: Bearer 9e9d7bfc-bc8e-38c1-ab67-909e0feb0fdd'



'''
