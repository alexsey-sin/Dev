import requests
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class ThreadLoadMOEX(QObject):
    int_value = pyqtSignal(int)
    message_value = pyqtSignal(str)
    text_value = pyqtSignal(str)
    dict_value = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def run(self):
        listSecIdBonds = []
        listBonds = {}
        listSecIdBonds = self.GetMOEXsecidBonds()
        listBonds = self.GetMOEXBonds(listSecIdBonds)
        self.dict_value.emit(listBonds)

    def GetMOEXsecidBonds(self):
        str_url = "http://iss.moex.com/iss/securities.json"
        outList = []
        start = 7600
        limit = 100
        search_parameters = {
            'lang': 'ru',
            'group_by': 'group',
            'group_by_filter': 'stock_bonds',
        }

        while(True):
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
                self.message_value.emit(f'Загружаем предварительный список: {len(outList)+cnt}')
                for i in range(cnt):
                    sec_id = res['securities']['data'][i][ind_sec_id]
                    outList.append(sec_id)
                    self.message_value.emit(sec_id)
            except Exception as exc:
                self.message_value.emit(f'Ошибка загрузки списка: {exc}')
                print(exc)
                break

            start += limit
        return outList

    def GetMOEXBonds(self, listSecId):
        # For example can be substituted RU000A101PV6.json
        str_url_tmp = "http://iss.moex.com/iss/securities/"
        outListBOND = {}

        for sec_id in listSecId:
            try:
                str_url = f'{str_url_tmp}{sec_id}.json'
                response = requests.get(str_url)
                if response.status_code != 200:
                    raise Exception(f'Ответ сервера: {response.status_code}')
                res = response.json()

                self.message_value.emit(f'Обработка: {sec_id}')
                cnt_field = 0
                dict_bond = {}
                # перелистаем поля бумаги
                for fldBond in res['description']['data']:
                    if fldBond[0] == 'SECID' and sec_id == fldBond[2]:
                        cnt_field += 1
                    if fldBond[0] == 'NAME':
                        dict_bond['NAME'] = fldBond[2]
                        cnt_field += 1
                    if fldBond[0] == 'MATDATE':
                        dict_bond['MATDATE'] = fldBond[2]
                        cnt_field += 1
                    if fldBond[0] == 'FACEVALUE':
                        dict_bond['FACEVALUE'] = fldBond[2]
                        cnt_field += 1
                    if fldBond[0] == 'COUPONFREQUENCY':
                        dict_bond['COUPONFREQUENCY'] = fldBond[2]
                        cnt_field += 1
                    if fldBond[0] == 'COUPONVALUE':
                        dict_bond['COUPONVALUE'] = fldBond[2]
                        cnt_field += 1
                    if fldBond[0] == 'TYPE':
                        dict_bond['TYPE'] = fldBond[2]
                        cnt_field += 1

                if cnt_field == 7:
                    outListBOND[sec_id] = dict_bond

            except Exception as exc:
                self.message_value.emit(f'Ошибка загрузки {sec_id}: {exc}')
                print(exc)
        return outListBOND
