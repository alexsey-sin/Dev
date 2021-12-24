import os
import time
from datetime import datetime
from tkinter import *


def clicked():  
    lbl.configure(text="Я же просил...") 

window = Tk()
window.geometry('400x250')
window.title("Добро пожаловать в приложение PythonRu")
lbl = Label(window, text="Привет", font=("Arial Bold", 20))
lbl.grid(column=0, row=0)
btn = Button(window, text="Не нажимать!")
btn.grid(column=1, row=0)
window.mainloop()
    
# # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
# TELEGRAM_CHAT_ID = '1740645090'
# TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# PERIOD_BETWEEN = 2

# if __name__ == '__main__':
    # while True:
        # time.sleep(PERIOD_BETWEEN)
        # # Рабочее время ботов с 6 до 23
        # cur_time = datetime.now()
        # if cur_time.hour < 6 or cur_time.hour >= 23: continue
        # str_time = cur_time.strftime('%H:%M:%S %d-%m-%Y')
        
        # #===============================================#
        # # Скрипт Проверка ТхВ beeline
        # if start_time_txv_beeline:
            # passed = (cur_time - start_time_txv_beeline).seconds
        # if start_time_txv_beeline == None or passed >= PERIOD_SCAN_TXV_BEELINE:
            # start_time_txv_beeline = cur_time
            # print(f'start txv_beeline {str_time}')
            # run_txv_beeline(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_beeline(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#
        # # Скрипт Проверка ТхВ mts
        # if start_time_txv_mts:
            # passed = (cur_time - start_time_txv_mts).seconds
        # if start_time_txv_mts == None or passed >= PERIOD_SCAN_TXV_MTS:
            # start_time_txv_mts = cur_time
            # print(f'start txv_mts {str_time}')
            # run_txv_mts(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_mts(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#

        # # Скрипт Проверка ТхВ domru
        # if start_time_txv_domru:
            # passed = (cur_time - start_time_txv_domru).seconds
        # if start_time_txv_domru == None or passed >= PERIOD_SCAN_TXV_DOMRU:
            # start_time_txv_domru = cur_time
            # print(f'start txv_domru {str_time}')
            # run_txv_domru(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_domru(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#

        # # Скрипт Проверка ТхВ rostelecom
        # if start_time_txv_rostelecom:
            # passed = (cur_time - start_time_txv_rostelecom).seconds
        # if start_time_txv_rostelecom == None or passed >= PERIOD_SCAN_TXV_ROSTELECOM:
            # start_time_txv_rostelecom = cur_time
            # print(f'start txv_rostelecom {str_time}')
            # run_txv_rostelecom(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_rostelecom(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#

        # # Скрипт Проверка ТхВ ttk
        # if start_time_txv_ttk:
            # passed = (cur_time - start_time_txv_ttk).seconds
        # if start_time_txv_ttk == None or passed >= PERIOD_SCAN_TXV_TTK:
            # start_time_txv_ttk = cur_time
            # print(f'start txv_ttk {str_time}')
            # run_txv_ttk(BID_TELEGRAM_CHAT_ID, BID_TELEGRAM_TOKEN)
            # # run_txv_ttk(TELEGRAM_CHAT_ID, TELEGRAM_TOKEN)
            # continue

        # #===============================================#

    #####################################################
