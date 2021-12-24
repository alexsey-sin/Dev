from os import path
import requests
import sqlite3 as sl
import re
import string
import datetime as dt
from datetime import *


query_create_table = ('CREATE TABLE IF NOT EXISTS bond '
                      '(id INTEGER PRIMARY KEY, '
                      'sec_id TEXT, '
                      'name TEXT, '
                      'm_date TEXT, '
                      'nominal INTEGER, '
                      'coup_freq INTEGER, '
                      'coup_val REAL, '
                      'type TEXT, '
                      'profit REAL)'
                      )


def load_net(con, cur) -> bool:
    """ Обновление таблицы bond """

    is_yes = input('Очистить базу и загрузить новый список? (y / n): ')
    if is_yes != 'y':
        return False

    # Очистим таблицу bond
    cur_db.execute('DELETE FROM bond;')
    cur_db.execute('REINDEX bond;')
    con.commit()

    list_secid = []
    str_url = "http://iss.moex.com/iss/securities.json"
    start = 0   # 7700
    limit = 100
    search_parameters = {
        'lang': 'ru',
        'group_by': 'group',
        'group_by_filter': 'stock_bonds',
    }

    while True:
        try:
            search_parameters['limit'] = limit
            search_parameters['start'] = start
            response = requests.get(str_url, params=search_parameters)
            if response.status_code != 200:
                raise Exception(f'Ответ сервера: {response.status_code}')
            res = response.json()
            ind_sec_id = res['securities']['columns'].index('secid')
            cnt = len(res['securities']['data'])
            if cnt == 0:
                break
            for i in range(cnt):
                sec_id = res['securities']['data'][i][ind_sec_id]
                list_secid.append(sec_id)
        except Exception as exc:
            print(f'Ошибка загрузки списка: {exc}')
            break

        start += limit

    str_url_tmp = "http://iss.moex.com/iss/securities/"
    for sec_id in list_secid:
        query_i = None
        try:
            str_url = f'{str_url_tmp}{sec_id}.json'
            response = requests.get(str_url)
            if response.status_code != 200:
                raise Exception(f'Ответ сервера: {response.status_code}')
            res = response.json()
            cnt_field = 0
            d_bnd = {}
            # перелистаем поля бумаги
            for fldBond in res['description']['data']:
                if fldBond[0] == 'SECID' and sec_id == fldBond[2]:
                    cnt_field += 1
                if fldBond[0] == 'NAME':
                    d_bnd['NAME'] = fldBond[2].replace('"', '')
                    cnt_field += 1
                if fldBond[0] == 'MATDATE':
                    d_bnd['MATDATE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'FACEVALUE':
                    d_bnd['FACEVALUE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'COUPONFREQUENCY':
                    d_bnd['COUPONFREQUENCY'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'COUPONVALUE':
                    d_bnd['COUPONVALUE'] = fldBond[2]
                    cnt_field += 1
                if fldBond[0] == 'TYPE':
                    d_bnd['TYPE'] = fldBond[2]
                    cnt_field += 1

            # Все поля найдены
            if cnt_field < 7:
                continue
            # отфильтруем только актуальные облигации
            m_date = datetime.strptime(d_bnd['MATDATE'], '%Y-%m-%d').date()
            if m_date < datetime.today().date():
                continue
            # Номинал должен быть нормальным числом
            nom = int(float(d_bnd['FACEVALUE']))
            if nom < 1:
                continue
            # Без выплаты купона тоже не интересны
            coup_freq = int(d_bnd['COUPONFREQUENCY'])
            if coup_freq < 1:
                continue
            # С нулевым купоном тоже не надо
            coup = float(d_bnd['COUPONVALUE'])
            if coup < 1:
                continue
            # Вычислим доходность облигации при покупке в 100%
            prof_per = round((coup * coup_freq * 100) / nom, 2)
            # Составим запрос для добавления в базу данных
            query_i = ('INSERT INTO bond (sec_id, name, m_date, nominal, '
                       'coup_freq, coup_val, type, profit) '
                       f'VALUES ("{sec_id}", "{d_bnd["NAME"]}", "{d_bnd["MATDATE"]}", '
                       f'{nom}, {coup_freq}, {coup}, "{d_bnd["TYPE"]}", {prof_per})')
            cur.execute(query_i)
        except Exception as exc:
            print(query_i)
            print(f'Ошибка загрузки {sec_id}: {exc}')
    con.commit()
    return True


def out_db(cur):
    query_s = 'SELECT * FROM bond'
    cur.execute(query_s)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def out_db_select(cur):
    # Здесь ввести список типов которые будут отобраны в результат
    types = "('corporate_bond', 'exchange_bond')"
    # types = "('exchange_bond', 'ofz_bond')"
    # types = "('exchange_bond')"

    query_s = f'SELECT * FROM bond WHERE type IN {types} ORDER BY profit DESC'
    cur.execute(query_s)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def out_types(cur):
    query_s = 'SELECT type FROM bond'
    cur.execute(query_s)
    rows = cur.fetchall()
    type_set = set(r[0] for r in rows)
    print(type_set)


def out_help():
    print('net - загрузка и обновление базы данных\n'
          'q - выход\n'
          'p - вывести все записи\n'
          't - вывести доступные типы\n'
          'cnt - количество записей\n'
          '===========================')


if __name__ == '__main__':
    file_db = 'moex.db'
    if not path.isfile(file_db):
        ans = input('Базы данных нет, создать? (y / n): ')
        if ans != 'y':
            exit(0)
    is_update = False
    con_db = sl.connect(file_db)
    cur_db = con_db.cursor()
    cur_db.execute(query_create_table)
    print('Облигации ММВБ. (help - справка)')

    while True:
        com = input('>>> ')
        if com == 'help':
            out_help()
        elif com == 'cnt':
            query = 'SELECT COUNT(*) AS cnt FROM bond;'
            records = cur_db.execute(query).fetchall()
            print('В базе данных бумаг:', records[0][0])
        elif com == 'net':
            is_update = load_net(con_db, cur_db)
        elif com == 'p':
            out_db(cur_db)
        elif com == 'ps':
            out_db_select(cur_db)
        elif com == 't':
            out_types(cur_db)
        elif com == 'q':
            break

    if is_update:
        cur_db.execute('VACUUM')
    con_db.close()
