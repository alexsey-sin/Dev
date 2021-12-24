import requests
import os
from dotenv import load_dotenv 
load_dotenv()


def get_friends(user_id):
    data = {
        'user_id': user_id,
        'v': os.getenv('API_V'),
        'access_token': os.getenv('TOKEN')
    }
    friends_list = requests.post(os.getenv('BASE_URL'), data=data)
    return friends_list.json()['response']
 
print(get_friends(531301803))  # запрашиваем список друзей пользователя с ID 531301803

