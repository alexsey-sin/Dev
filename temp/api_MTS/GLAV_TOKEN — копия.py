import requests
import json

cookie = "AQIC5wM2LY4Sfcx4IivFUYiFD6TCLUeMYRzgsHqyzWCIrG8.*AAJTSQACMDQAAlNLABMxNTczMjMwMTQwOTgxODAxMDU3AAJTMQACMjU.*"

headers = {
    "Content-Type": "application/json",
    "Cookie": f"MTSWebSSO={cookie}",
    "Authorization": "Bearer 35734616-e607-3451-b838-a564b7f66c8e",
    "Host": "login.mts.ru:443",
    "Connection": "Keep-Alive",
    "User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)",
}
data_post = {
    "client_owner": "domconnect",
    "email": "adm.tt76@gmail.com",
}
url_post = "https://login.mts.ru:443/wss/api-manager/PublicApi/Sandbox/WebSSORegistration/v1"

responce = requests.post(url_post, headers=headers, data=json.dumps(data_post))
print(responce.status_code)
print(responce.text)
with open("oauth_mts_api2.txt", "w", encoding="utf-8") as file:
    json.dump(responce.text, file)






# Номер:
# +7 910 963 0112


# https://lk-b2b.mts.ru		79109630404	!3W^f-QN

# Для номера главного 79109630404
# c:\Dev\parsing_MTS>python test.py
# 200
# {"client_name":"7604350152_79109630404","client_id":"cVAVjTPcRSk3xp0p3XzQcUQzz9pO0IyOiUpb6XGstUj0YUlyLkQsIJIzVcgRFgia@app.b2b.mts.ru","client_secret":"rRL2KKRlf7TPFa6U7MMWlBl7gNHl77gF1aZbXo5VpcXOUvTp4ncgj9SU7Kb8DxCmsEYrCsnS9nUh7K21l6dMZmdxsIMz4ujXDtOMwRzXVBBpMIz9NldcM8ITIxbRGQiDTtWhNOhIfFoZHPEH8vh4VS6CPWAs550r3sHJxmWOINiybaV8D9Wkk7ibScr0vUX2ydVFGZejahdbLZmSeD6FYEo5iEW1mR1XWvXkb3g2hEhG0y3mIGBopIBRwCkNsPmc","access_token":"AQIC5wM2LY4SfcyA5VXFqpPaAodKeLOv3agBveXc_tu1LdQ.*AAJTSQACMDQAAlNLABM0NjUwMDAyNDQ5MzgzOTc2MjY2AAJTMQACMjU.*","token_type":"Bearer","refresh_token":"VwwG8g2i1RHvmLSEp4xlphP5UDflLHvmIXo5tPqUfMwjFEijDJf5RuuM1gwobh98"}

# c:\Dev\parsing_MTS>
