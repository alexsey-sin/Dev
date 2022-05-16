# Работа с датой/временем в Python
# import os
# import time
# from datetime import datetime
# import time
# import datetime     # это модуль (это то, что у вас есть прямо сейчас).
from datetime import datetime, timedelta  # это класс.



# Строку в дату
s_date = '23.01.2022'
# dt = datetime.datetime.strptime(s_date, '%d.%m.%Y')
dt = datetime.strptime(s_date, '%d.%m.%Y')
# print(type(dt))
# print(dt)

dt2 = dt + timedelta(days=10)

# Прибавим несколько дней

# Дату в строку
s = dt2.strftime('%d.%m.%Y')
# print(s)  # -> '19.08.2018'



import calendar
cal = calendar.Calendar()
now = datetime.now()
# Количество рабочих дней в текущем месяце
working_days = len([x for x in cal.itermonthdays2(now.year, now.month) if x[0] !=0 and x[1] < 5])
# print('Рабочих дней: ', working_days)
cur_day = now.day      # Номер текущего дня
cur_month = now.month  # Номер текущего меяца
cur_year = now.year    # Номер текущего года
cnt_days_in_cur_month = calendar.monthrange(cur_year, cur_month)[1] # Количество дней в текущем месяце
# print(cur_day, cur_month, cur_year)

# Получение следующего и прошлого месяца
    # cur_date = datetime.today()
    # to_date = datetime(cur_date.year, cur_date.month, 1)
    # next_month = datetime.datetime(cur_date.year + int(cur_date.month / 12), ((cur_date.month % 12) + 1), 1)
    # last_month = datetime(cur_date.year - (not cur_date.month - 1), (cur_date.month - 1 or 12), 1)


'''
    %A  День недели как полное название локали. Среда
    %a  День недели как сокращенное название локали. Пн, вт, ср
    %w  День недели в виде десятичного числа, где 0 — воскресенье, а 6 — суббота. 0,1,2,3,4… 6
    %d  День месяца в виде десятичного числа с нулями. 01,02,03… 31
    %-d День месяца в виде десятичного числа. (Зависит от платформы) 1,2,3…
    %b  Месяц как сокращенное название языкового стандарта. Море 
    %B  Месяц как полное название локали. марш
    %m  Месяц как десятичное число с нулями. 01,02… 12
    %-m Месяц как десятичное число. (Зависит от платформы) 1,2,… 12
    %y  Год без века как десятичное число с нулями. 20 (на 2020 год)
    %Y  Год со столетием в виде десятичного числа. 2020, 2021 и др.
    %H  Час (в 24-часовом формате) как десятичное число с нулями. 01, 02,…
    %-H Час (24-часовой формат) в виде десятичного числа. (Зависит от платформы) 1,2,3,…
    %I  Час (12-часовой формат) как десятичное число с нулями. 01, 02, 03,…
    %-I Час (12-часовой формат) в виде десятичного числа. (Зависит от платформы) 1, 2, 3…
    %p  Локальный эквивалент AM или PM. ДО ПОЛУДНЯ ПОСЛЕ ПОЛУДНЯ
    %M  Минута в виде десятичного числа с нулями. 01, 02,… 59
    %-M Минута как десятичное число. (Зависит от платформы) 1,2,3,… 59
    %S  Второй — десятичное число с нулями. 01, 02,… 59
    %-S Секунда как десятичное число. (Зависит от платформы) 1, 2,… 59
    %f  Микросекунда в виде десятичного числа с нулями слева. 000000
    %z  Смещение UTC в форме + ЧЧММ или -ЧЧММ (пустая строка, если объект наивен). (пусто), +0000, -0400, +1030
    %Z  Название часового пояса (пустая строка, если объект наивный). (пусто), UTC, IST, CST
    %j  День года в виде десятичного числа с нулями. 1, 2, 3,… 366
    %-j День года в виде десятичного числа. (Зависит от платформы) 1, 2, 3,… 366
    %U  Номер недели в году (воскресенье как первый день недели) в виде десятичного числа, дополненного нулями. Все дни нового года, предшествующие первому воскресенью, считаются нулевой неделей. 1, 2, 3,… 53
    %W  Номер недели в году (понедельник как первый день недели) в виде десятичного числа. Все дни нового года, предшествующие первому понедельнику, считаются нулевой неделей. 1, 2, 3,… 53
    %c  Соответствующее представление даты и времени для локали. Ср 06 мая 12:23:56 2020
    %x  Соответствующее представление даты языкового стандарта. 06.05.20
    %X  Соответствующее временное представление локали. 12:23:56
    %%  Буквальный символ «%». %
'''

import os
# Количество месяцев между двумя датами
# from dateutil import rrule
date_start = datetime(2020, 12, 31)
date_now = datetime.today()
# months = rrule.rrule(rrule.MONTHLY, dtstart=date_start, utils=date_now).count()
months = (date_now.year - date_start.year) * 12 + date_now.month - date_start.month

folder_path = 'seo_archive'
dy = date_now - timedelta(days=1)
filename = dy.strftime(f'{folder_path}/%d-%m-%Y.json')
if not os.path.exists(folder_path): #Если пути не существует создаем его
    os.makedirs(folder_path)


# directory_folder = r"c:\Folder\file.txt"
# folder_path = os.path.dirname(directory_folder) # Путь к папке с файлом
# print('folder_path', folder_path)
# if not os.path.exists(folder_path): #Если пути не существует создаем его
    # os.makedirs(folder_path)

# with open(filename, 'w') as file: # Открываем фаил и пишем
    # file.write("этот текст создан автоматически")
print(filename)

import datetime

delta = datetime.timedelta(days=0, 
                           seconds=0, 
                           microseconds=0, 
                           milliseconds=0, 
                           minutes=0, 
                           hours=0, 
                           weeks=0)

    # cur_date = datetime.today()
    to_date = datetime(cur_date.year, cur_date.month, 1).date()
    from_date = datetime(cur_date.year - (not cur_date.month - 1), (cur_date.month - 1 or 12), 1).date()


