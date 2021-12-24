import requests
import json


headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "login.mts.ru",
    "Connection": "Keep-Alive",
    "User-Agent": "Apache-HttpClient/4.1.1 (java 1.5)",
}
data = "grant_type=refresh_token&client_id=cVAVjTPcRSk3xp0p3XzQcUQzz9pO0IyOiUpb6XGstUj0YUlyLkQsIJIzVcgRFgia@app.b2b.mts.ru&client_secret=rRL2KKRlf7TPFa6U7MMWlBl7gNHl77gF1aZbXo5VpcXOUvTp4ncgj9SU7Kb8DxCmsEYrCsnS9nUh7K21l6dMZmdxsIMz4ujXDtOMwRzXVBBpMIz9NldcM8ITIxbRGQiDTtWhNOhIfFoZHPEH8vh4VS6CPWAs550r3sHJxmWOINiybaV8D9Wkk7ibScr0vUX2ydVFGZejahdbLZmSeD6FYEo5iEW1mR1XWvXkb3g2hEhG0y3mIGBopIBRwCkNsPmc&refresh_token=VwwG8g2i1RHvmLSEp4xlphP5UDflLHvmIXo5tPqUfMwjFEijDJf5RuuM1gwobh98"

url = "https://login.mts.ru/amserver/oauth2/token"

responce = requests.post(url, headers=headers, data=data)
print(responce.status_code)
print(responce.text)
with open("oauth_refresh.txt", "w", encoding="utf-8") as file:
    json.dump(responce.text, file)


# c:\Dev\parsing_MTS>python REFRESH_ACCESS.py
# 200
# {"access_token":"AQIC5wM2LY4SfcxPFfh9bjvKKdeCY4IH19rR7eLqmrlaEUM.*AAJTSQACMDQAAlNLABMtNTUwMjIzMTAyNTgzOTc1MDk0AAJTMQACMTE.*","expires_in":14400,"token_type":"Bearer","refresh_token":"VwwG8g2i1RHvmLSEp4xlphP5UDflLHvmIXo5tPqUfMwjFEijDJf5RuuM1gwobh98"}

# c:\Dev\parsing_MTS>








