import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []
        self.date_today = dt.date.today()

    def add_record(self, expenses):
        self.records.append(expenses)

    def get_today_stats(self):
        # expens_today = []
        # for item in self.records:
        #     if item.date == self.date_today:
        #         expens_today.append(item.amount)
        # return sum(expens_today)
        # Ниже привиден метод  'list comprehension'
        # новый_список = [«операция» for «элемент списка» in «список» if «условие»]
        return sum([item.amount for item in self.records if item.date == self.date_today])

    def get_today_remaind(self):
        today_remaind = self.limit - self.get_today_stats()
        return today_remaind

    def get_week_stats(self):
        week_stats = []
        one_week = dt.date.today() - dt.timedelta(days=7)
        for item in self.records:
            if one_week <= item.date <= self.date_today:
                week_stats.append(item.amount)
        return sum(week_stats)


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.get_today_remaind()
        if calories_remained > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей'
                    f' калорийностью не более {calories_remained} кКал')

        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    RUB_RATE = 1.0
    EURO_RATE = 70.0
    USD_RATE = 60.0

    def get_today_cash_remained(self, currency):
        currency_dict = {
            'rub': [self.RUB_RATE, 'руб'],
            'usd': [self.USD_RATE, 'USD'],
            'eur': [self.EURO_RATE, 'Euro']
        }
        limit_remained = self.get_today_remaind()
        value, cur_name = currency_dict.get(currency)
        convert_maney = round(limit_remained / value, 2)
        if limit_remained == 0:
            return 'Денег нет, держись'
        elif limit_remained > 0:
            return ('На сегодня осталось'
                    f' {convert_maney} {cur_name}')
        elif currency not in currency_dict:
            return 'Запрашиваемой валюты нет.'
        else:
            convert_maney = abs(convert_maney)
            return ('Денег нет, держись: твой долг - '
                    f'{convert_maney} {cur_name}')


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


if __name__ == '__main__':
    cash_calculator = CashCalculator(100)
    cash_calculator.add_record(Record(amount=145, comment='кофе'))
    cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
    cash_calculator.add_record(
        Record(amount=3000, comment='бар в Танин др', date='01.09.2019'))

    print(cash_calculator.get_today_cash_remained('rub'))

    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(amount=145, comment='кофе'))
    calories_calculator.add_record(
        Record(amount=300, comment='Серёге за обед'))
    calories_calculator.add_record(
        Record(amount=3000, comment='бар в Танин др', date='01.09.2019'))

    print(calories_calculator.get_calories_remained())
