import requests, json, time, logging
from datetime import datetime


# url_host = 'http://127.0.0.1:8000/'
url_host = 'http://django.domconnect.ru/'

def get_token():  # Получение токена по логину и паролю
    login = 'YrxF9TvrPlK6fbkJNBilUqCw0vUa'
    password = 'hFtsFhai1ZjtuYg_y58fArkaBCEa'
    url = 'https://api.mts.ru/token'

    mess = ''
    token = ''
    auth = (login, password)
    data = {'grant_type': 'client_credentials'}

    try:
        resp = requests.post(url, auth=auth, data=data, timeout=30)
        if resp.status_code == 200:
            dct_answer = json.loads(resp.text)
            token = dct_answer.get('access_token')
            expires_in = dct_answer.get('expires_in')
            # print(expires_in)
            if token == None:
                fault = dct_answer.get('fault')
                if fault: mess = f'ERROR: {fault.get("message")} {fault.get("description")}'
        else: mess = f'ERROR get_token: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_token: try: {str(e)}'
    return mess[:200], token

def get_bill_plan_info(token, msisdn):  # Запрос действующего тарифного плана
    url = 'https://api.mts.ru/b2b/v1/Product/BillPlanInfo'
    mess = ''
    plan = None
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'ChannelId': 'NCIH_National_PAPI',
        'Authorization': f'Bearer {token}',
    }
    params = {
        'productCharacteristic.name': 'MSISDN',
        'productCharacteristic.value': msisdn,
        'fields': 'productCharacteristic,place.role,place.externalID,productOffering.name,productOffering.href,productOffering.externalID,productOffering.validFor',
        'productLine.name': 'MobileConnectivity',
    }
    # , data={}
    cnt_try = 5
    try:
        while cnt_try:
            cnt_try -= 1
            resp = requests.get(url, headers=headers, params=params, timeout=300)
            if resp.status_code == 200: break
            time.sleep(2)

        if resp.status_code == 200:
            dct_answer = json.loads(resp.text)
            if type(dct_answer) != dict: raise Exception('Invalid answer 1')
            prOff = dct_answer.get('productOffering')
            if type(prOff) != dict: raise Exception('Invalid answer 2')
            name = prOff.get('name')
            if name == None or type(name) != str or len(name) == 0: raise Exception('Invalid answer 3')
            plan = name.split('(')[0].strip()
            if len(plan) == 0: raise Exception('Invalid answer 4')
        else: mess = f'ERROR get_bill_plan_info: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_bill_plan_info: try: {str(e)}'
    return mess[:200], plan

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
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code == 200:
            lst_answer = json.loads(resp.text)
            if type(lst_answer) == list and len(lst_answer) > 0: dct_answer = lst_answer[0]
            else: raise Exception('Invalid answer 1')
            lst_cuAccBal = dct_answer.get('customerAccountBalance')
            if lst_cuAccBal == None or type(lst_cuAccBal) != list: raise Exception('Invalid answer 2')
            dct_cuAccBal = lst_cuAccBal[0]
            if type(dct_cuAccBal) != dict: raise Exception('Invalid answer 3')
            dct_rmAmount = dct_cuAccBal.get('remainedAmount')
            if type(dct_rmAmount) != dict: raise Exception('Invalid answer 4')
            amount = dct_rmAmount.get('amount')
            if amount == None: raise Exception('Invalid answer 5')
        else: mess = f'ERROR get_balance: requests.status_code: {resp.status_code}'
    except Exception as e:
        mess = f'ERROR get_balance: try: {str(e)}'
    return mess[:200], amount

def get_validity_info(token, msisdn, tarif):  # Получение остатков пакетов минут, интернет, смс по номеру MSISDN (7...)
    url = 'https://api.mts.ru/b2b/v1/Bills/ValidityInfo'
    mess = ''
    dct_info = {
        'number': msisdn,
        'mobile_available': 0,
        'mobile_total': 0,
        'sms_available': 0,
        'sms_total': 0,
        'info_mess': '',
    }
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
     # data={},
    cnt_try = 5
    try:
        while cnt_try:
            cnt_try -= 1
            resp = requests.get(url, headers=headers, params=params, timeout=300)
            if resp.status_code == 200: break
            time.sleep(2)

        if resp.status_code == 200:
            while True:
                lst_answer = json.loads(resp.text)
                if type(lst_answer) != list: dct_info['info_mess'] = 'lst_answer is not list'; break
                for item in lst_answer:
                    if type(item) != dict: dct_info['info_mess'] = 'item lst_answer is not dict'; break
                    name = item.get('name')
                    if name != 'ForisCounters': continue # Блок с счетчиками (есть еще блок h2oProfile - много разной всячины)
                    cuAcc = item.get('customerAccount')
                    if cuAcc == None or type(cuAcc) != list or len(cuAcc) != 1: raise Exception('Invalid answer 3')
                    prRel = cuAcc[0].get('productRelationship')
                    if prRel == None or type(prRel) != list or len(prRel) == 0: dct_info['info_mess'] = 'invalid productRelationship'; break
                    for rel in prRel:
                        prod = rel.get('product')
                        if type(prod) != dict: continue
                        prodSpec = prod.get('productSpecification')
                        if type(prodSpec) != dict: continue
                        tarPlan = prodSpec.get('name')
                        if tarPlan == None: continue
                        ipl = tarPlan.find(tarif)
                        if ipl >= 0:
                            imin = tarPlan.find('мин')
                            if imin >= 0:
                                prodSpecChr = prodSpec.get('productSpecCharacteristic')
                                if type(prodSpecChr) != list: continue
                                for pSpecChr in prodSpecChr:
                                    prodSpecChrVal = pSpecChr.get('prodSpecCharacteristicValue')
                                    if type(prodSpecChrVal) != list: continue
                                    for pscv in prodSpecChrVal:
                                        valTp = pscv.get('valueType')
                                        if valTp == 'PeriodInitialValue':
                                            val = pscv.get('value')
                                            try: val = int(val)
                                            except: raise Exception('Invalid answer 5')
                                            dct_info['mobile_total'] = int(val/60)
                                        if valTp == 'CurrentValue':
                                            val = pscv.get('value')
                                            try: val = int(val)
                                            except: raise Exception('Invalid answer 6')
                                            dct_info['mobile_available'] = int(val/60)
                            imin = tarPlan.find('смс')
                            if imin >= 0:
                                prodSpecChr = prodSpec.get('productSpecCharacteristic')
                                if type(prodSpecChr) != list: continue
                                for pSpecChr in prodSpecChr:
                                    prodSpecChrVal = pSpecChr.get('prodSpecCharacteristicValue')
                                    if type(prodSpecChrVal) != list: continue
                                    for pscv in prodSpecChrVal:
                                        valTp = pscv.get('valueType')
                                        if valTp == 'PeriodInitialValue':
                                            val = pscv.get('value')
                                            try: dct_info['sms_total'] = int(val)
                                            except: raise Exception('Invalid answer 7')
                                        if valTp == 'CurrentValue':
                                            val = pscv.get('value')
                                            try: dct_info['sms_available'] = int(val)
                                            except: raise Exception('Invalid answer 8')
                with open('validity_info2.json', 'w', encoding='utf-8') as out_file:
                    json.dump(lst_answer, out_file, ensure_ascii=False, indent=4)
                # print(json.dumps(lst_answer, indent=2))
                break
                        

        else: mess = f'ERROR get_validity_info: requests.status_code: {resp.status_code} {resp.text}'
    except Exception as e:
        mess = f'ERROR get_validity_info: try: {str(e)}'
    return mess[:200], dct_info

def send_telegram(chat: str, token: str, text: str):
    url = "https://api.telegram.org/bot" + token + "/sendMessage"
    try:
        r = requests.post(url, data={
            "chat_id": chat,
            "text": text
        })
    except:
        return 600
    return r.status_code

def send_api(data):
    url = url_host + 'mobile/api'
    headers = {
        'Content-Type': 'application/json',
        'Connection': 'Keep-Alive',
        'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
    }
    try:
        res = requests.post(url, headers=headers, json=data)
        if res.status_code != 200: raise Exception(f'requests.status_code:{res.status_code}')
    except Exception as e: return str(e)[:100]
    
    return ''

def run_lk_mts(logger, tlg_chat, tlg_token):
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
    
    mob_numbers = [
        '79109631515',
        '79109630808',
        '79109630707',
        '79109630633',
        '79109630505',
        '79109630500',
        '79109630404',
        '79109630307',
        '79109630112',
        '79108100395',
        '76850047000',
    ]
    
    # Получаем токен
    e, token = get_token()
    if e:
        mess = f'run_lk_mts ERROR: {e}'
        send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
        logger.error(mess)
        return
    time.sleep(2)

    # Начальные данные
    out_dict = {
        'operator': 'mts',
        'numbers': [],
    }
    res_mess = 'Parsing mts:\n'
    cnt_avlb_min = 0
    cnt_totl_min = 0
    cnt_avlb_sms = 0
    cnt_totl_sms = 0
    
    # Проход по всем номерам
    for mob_num in mob_numbers:
        # Возьмем баланс
        e, balance = get_balance(token, mob_num)
        if e:
            mess = f'run_lk_mts ERROR: {e}'
            send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
            logger.error(mess)
            return
        time.sleep(2)
        
        if mob_num == mob_numbers[0]:
            res_mess += f'balance: {balance}\n'
        # Возьмем тарифный план (пакет)
        e, plan = get_bill_plan_info(token, mob_num)
        if e:
            mess = f'run_lk_mts ERROR: {e}'
            send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
            logger.error(mess)
            return
        time.sleep(2)
        
        # Возьмем остатки минут, смс
        e, dct_info = get_validity_info(token, mob_num, plan)
        if e:
            mess = f'run_lk_mts ERROR: {e}'
            send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
            logger.error(mess)
            return
        time.sleep(2)
        # Добавим в суммарные данные
        cnt_avlb_min += dct_info['mobile_available']
        cnt_totl_min += dct_info['mobile_total']
        cnt_avlb_sms += dct_info['sms_available']
        cnt_totl_sms += dct_info['sms_total']
        
        dct_info['balance'] = balance  # Добавим баланс
        out_dict['numbers'].append(dct_info)  # И внесем в общий список
        ma = dct_info["mobile_available"]
        mt = dct_info["mobile_total"]
        sa = dct_info["sms_available"]
        st = dct_info["sms_total"]
        if ma or mt or sa or st: res_mess += f'{mob_num} [min {ma}/{mt}][sms {sa}/{st}]\n'
    res_mess += f'Итого: [min {cnt_avlb_min}/{cnt_totl_min}][sms {cnt_avlb_sms}/{cnt_totl_sms}]\nВсего номеров: {len(mob_numbers)}'
    e = send_api(out_dict)
    if e:
        mess = f'run_lk_mts ERROR: send_api: {e}'
        send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
        logger.error(mess)
        return
    send_telegram(tlg_chat, tlg_token, res_mess)  # Отправим полученные данные в чат
    logger.info(res_mess)  # В лог тоже
    
    

if __name__ == '__main__':
    start_time = datetime.now()
    # личный бот @infra
    TELEGRAM_CHAT_ID = '1740645090'
    TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

    logging.basicConfig(
        level=logging.INFO,     # DEBUG, INFO, WARNING, ERROR и CRITICAL По возрастанию
        filename='log_main.log',
        datefmt='%d.%m.%Y %H:%M:%S',
        format='%(asctime)s:%(levelname)s:\t%(message)s',  # %(name)s:
    )
    logger = logging.getLogger(__name__)
    
    run_lk_mts(logger, TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
    
    end_time = datetime.now()
    dur_str = '\nDuration: {}'.format(end_time - start_time)
    print(dur_str)



    '''
        Ограничения тарифа "Бесплатно"
        до 60 вызовов в минуту
        до 3 вызовов в секунду

    '''


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
        
        Список подключенных услуг стр. 24
        
        Запрос действующего тарифного плана стр. 36

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

        структура отправляемых данных:
        data = {
            'operator': 'mts',
            'numbers': [
                {
                    'number': '76850047000',
                    'balance': '-23.25',
                    'mobile_available': '23',
                    'mobile_total': '467',
                    'sms_available': '0',
                    'sms_total': '0',
                },
                {
                    'number': '76850047000',
                },
                ...
            ]
        }


    '''
    '''
        Здравствуйте.
        Перешли на ваш новый продукт и уже не рады.
        АПИ нам нужно чтобы оперативно получать информацию по балансам и по остаткам минут и смс на телефонных номерах.
        Да улучшения есть в плане того что упростились запросы.
        Но! В новой версии пропали API функции по которым можно запросить перечень лицевых счетов
        и перечень своих номеров телефонов.
        А сейчас перестал сервер отвечать на запросы по https://api.mts.ru/b2b/v1/Bills/ValidityInfo
        Идут ответы 504 или 503 в дневные часы. Утром и вечером все работает.
        По этому запросу сервер возвращает много лишней информации общим объемом около мегабайта.
        Подскажите в чем дело?
        Просьба ответить на alexey-sin@yandex.ru
    '''
    pass