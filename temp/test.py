import requests, json, time, logging
from datetime import datetime


# личный бот @infra
TELEGRAM_CHAT_ID = '1740645090'
TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'
emj_red_mark = '❗️'
emj_red_ball = '🔴'
emj_yellow_ball = '🟡'
emj_green_ball = '🟢'
emj_red_rhomb = '♦️'
emj_yellow_rhomb = '🔸'

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


if __name__ == '__main__':
    mess = f'run_lk_mts ERROR: {emj_red_rhomb} {emj_yellow_rhomb} '
    rez = send_telegram(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, mess)
    if rez: print(rez)
