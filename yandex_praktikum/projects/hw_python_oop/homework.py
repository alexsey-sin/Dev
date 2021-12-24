import datetime as dt


class Record:
    def __init__(self, amount, date=None, comment=''):
        if date is None:
            new_date = dt.date.today()
        else:
            new_date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.amount = amount
        self.date = new_date
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        date_today = dt.date.today()
        amount_list = [r.amount for r in self.records if r.date == date_today]
        amount_today = sum(amount_list)
        return amount_today

    def get_week_stats(self):
        date_today = dt.date.today()
        date_start = date_today - dt.timedelta(weeks=1)
        amount_week = 0

        for rec in self.records:
            if date_start < rec.date <= date_today:
                amount_week += rec.amount
        return amount_week

    def get_today_remained(self):
        today_remained = self.limit - self.get_today_stats()
        return today_remained


class CashCalculator(Calculator):
    # exchange rates for 09.02.2021
    USD_RATE = 74.30
    EURO_RATE = 89.58

    def __init__(self, limit):
        super().__init__(limit)

    def get_today_cash_remained(self, currency):
        balance = self.get_today_remained()
        currency_dict = {
            'rub': ['руб', 1],
            'usd': ['USD', self.USD_RATE],
            'eur': ['Euro', self.EURO_RATE]}

        if currency not in currency_dict:
            return 'Unknown currency'

        str_currency = currency_dict[currency][0]
        balance /= currency_dict[currency][1]
        balance = round(balance, 2)

        if balance == 0:
            sentence = 'Денег нет, держись'
        elif balance > 0:
            sentence = f'На сегодня осталось {balance} {str_currency}'
        else:
            balance = abs(balance)
            sentence = ('Денег нет, держись: '
                        f'твой долг - {balance} {str_currency}')

        return sentence


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        balance = self.get_today_remained()

        if balance > 0:
            sentence = ('Сегодня можно съесть что-нибудь ещё, '
                        f'но с общей калорийностью не более {balance} кКал')
        else:
            sentence = 'Хватит есть!'

        return sentence


if __name__ == '__main__':
    pass
