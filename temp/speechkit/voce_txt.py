import os
import requests
from dotenv import load_dotenv
from txt_voice import get_iamToken
import json


load_dotenv()
Y_OA_TOKEN = os.getenv('YANDEX_OAUTH_TOKEN')
Y_IAM_URL = os.getenv('YANDEX_IAM_URL')
Y_ID_FOLDER = os.getenv('YANDEX_ID_FOLDER')
Y_STT_URL = os.getenv('YANDEX_STT_URL')


def main():
    name_file = 'speech.ogg'

    iam_token = get_iamToken(Y_OA_TOKEN, Y_IAM_URL)
    if iam_token == None:
        print('No token')
        return

    headers = {
        'Authorization': f'Bearer {iam_token}',
    }
    params = {
        'folderId': f'{Y_ID_FOLDER}',
    }
    with open(name_file, 'rb') as file:
        data = file.read()
        response = requests.post(Y_STT_URL, headers=headers, params=params, data=data)
    
    status = response.status_code
    if status == 200:
        js = json.loads(response.text)
        out_text = js.get('result')
        print(out_text)
    else:
        print(status)



if __name__ == '__main__':
    main()



