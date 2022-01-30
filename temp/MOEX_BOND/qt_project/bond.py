class Bond:
    def __init__(self, sec_id, matdate, facevalue,
                 couponfrequency, couponvalue, btype):
        self.sec_id = sec_id
        self.matdate = matdate
        self.facevalue = facevalue
        self.couponfrequency = couponfrequency
        self.couponvalue = couponvalue
        self.btype = btype

    @staticmethod
    def LoadFile(name_file):
        print(f"LoadFile {name_file}")

    @staticmethod
    def SaveFile(name_file):
        out_list = []
        print(f"SaveFile {name_file}")
        return out_list




"""
Словарь с облигациями будет иметь такую структуру:
d_dict = {
    'RU000A101PV6': {
        'NAME': "ТД РКС-Сочи БО-01"
        'MATDATE': "2023-05-23",
        'FACEVALUE': "1000",
        'COUPONFREQUENCY': "4",
        'COUPONVALUE': "34.9",
        'TYPE': "exchange_bond"
    }
    'RU000A101PV6': {
        'NAME': "ТД РКС-Сочи БО-01"
        'MATDATE': "2023-05-23",
        'FACEVALUE': "1000",
        'COUPONFREQUENCY': "4",
        'COUPONVALUE': "34.9",
        'TYPE': "exchange_bond"
    }
    ...
}
"""
