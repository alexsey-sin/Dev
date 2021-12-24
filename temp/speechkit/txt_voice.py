import os
from datetime import datetime as dt
from datetime import timedelta
import requests
import json
from dotenv import load_dotenv


load_dotenv()
Y_OA_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')
Y_IAM_URL = os.getenv('YANDEX_IAM_URL')
Y_ID_FOLDER = os.getenv('YANDEX_ID_FOLDER')
Y_TTS_URL = os.getenv('YANDEX_TTS_URL')

threshold_time_iam_token = timedelta(hours=2)


def get_iamToken(oa_token, iam_url):
    # Время жизни IAM-токена — не больше 12 часов, но рекомендуется запрашивать его чаще, например каждый час.
    iam_bad = False
    iam_token = None

    try:
        with open('time_token.json', 'r', encoding='utf-8') as file:  # читаем время создания токена если есть
            js = json.load(file)
        dt_old_str = js.get('time_create')
        dt_old = dt.strptime(dt_old_str, '%Y-%m-%d %H:%M:%S.%f')
        delta_dt = dt.now() - dt_old
        if delta_dt > threshold_time_iam_token:
            iam_bad = True
        else:
            iam_token = js.get('iam_token')
            print('Token read in file')
    except:
        iam_bad = True

    if iam_bad:
        data = {"yandexPassportOauthToken": oa_token}
        try:
            response = requests.post(iam_url, data=str(data))
            iam_token = response.json().get('iamToken')
            dict_token = {
                'time_create': str(dt.now()),
                'iam_token': iam_token
            }
            with open('time_token.json', 'w', encoding='utf-8') as file:
                json.dump(dict_token, file)
                print('Token download and save')
        except:
            print('error')
            pass
    
    return iam_token


def main():

    my_text = 'Здесь мы записываем результат, и зан+осим в таблицу'

    iam_token = get_iamToken(Y_OA_TOKEN, Y_IAM_URL)
    if iam_token == None:
        print('No token')
        return


    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    data = {
        'lang': 'ru-RU',
        'folderId': f'{Y_ID_FOLDER}',
        'text': f'{my_text}'
    }

    response = requests.post(Y_TTS_URL, headers=headers, data=data)

    with open('speech.ogg', 'wb') as f: #создаем файл для записи результатов
        f.write(response.content) #записываем результат

    print(response.status_code)




if __name__ == '__main__':
    main()




