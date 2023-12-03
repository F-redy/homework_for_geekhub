# 2. Створіть програму для отримання курсу валют за певний період.
# - отримати від користувача дату (це може бути як один день так і інтервал - початкова і кінцева дати,
# продумайте механізм реалізації) і назву валюти
# - вивести курс по відношенню до гривні на момент вказаної дати (або за кожен день у вказаному інтервалі)
# - не забудьте перевірку на валідність введених даних


import http
from datetime import datetime

import requests


class ExchangeRates:

    def __init__(self):
        self.today = datetime.now().date()
        self.available_currencies = self.get_available_currencies()
        self.available_codes = [data['cc'].upper() for data in self.available_currencies]

    @staticmethod
    def get_exchange_rate(date: str, currency_code: str):
        url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency_code}&date={date}&json'

        response = requests.get(url)

        if response.status_code == http.HTTPStatus.OK:
            exchange_rate = response.json()
            if exchange_rate:
                return exchange_rate[0]['rate']

        print('\nПомилка при отриманні даних з сервера')

    @staticmethod
    def get_exchange_rates(start_date: str, end_date: str, currency_code: str) -> list | None:
        url = (
            f'https://bank.gov.ua/NBU_Exchange/exchange_site?'
            f'start={start_date}&'
            f'end={end_date}&'
            f'valcode={currency_code}&'
            f'sort=exchangedate&'
            f'json'
        )

        response = requests.get(url)

        if response.status_code == http.HTTPStatus.OK:
            data = response.json()
            if data:
                return data
            else:
                print(f'{currency_code} ')
        else:
            print('\nПомилка при отриманні даних з сервера')

    def validate_date(self, date: str):
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()

            if date <= self.today:
                return date
            else:
                print('\nВведена дата з майбутнього.')
                return None

        except ValueError:
            print('\nНевірний формат дати.')
            return None

    def validate_code(self, code: str) -> str:
        if code.upper() in self.available_codes:
            return code
        print(f'\nВалютний код "{code}" не знайдено у списку доступних валют Національного банку України.')
        self.show_available_currencies()

    @staticmethod
    def get_available_currencies():
        url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        response = requests.get(url)
        if response.status_code == http.HTTPStatus.OK:
            return response.json()
        else:
            print('\nПомилка при отриманні даних з сервера')

    def show_available_currencies(self):
        if self.available_currencies:
            print('\nДоступні валюти:')
            for item in self.available_currencies:
                print(f'Код: {item["cc"]}, Назва: {item["txt"]}')

    @staticmethod
    def show_exchange_rates(start_date, end_date, currency_code, data_rate: list) -> None:
        print(f'\nКурс "{currency_code.upper()}" до гривні з {start_date} по {end_date}:')
        for item in data_rate:
            print(f'{item["exchangedate"]}: {item["rate"]}')

    def get_dates(self) -> datetime.date:
        valid_dates = []
        while not valid_dates:
            date_input = input(
                'Введіть дату у форматі "рік-місяць-день" або "початкова-дата кінцева-дата" '
                '(наприклад, 2023-12-01 або 2020-01-01 2023-12-01): '
            )
            dates = date_input.split()
            if len(dates) == 1:
                date = self.validate_date(dates[0])
                if date:
                    valid_dates.append(date)
            elif len(dates) == 2:
                start_date = self.validate_date(dates[0])
                end_date = self.validate_date(dates[1])
                if start_date and end_date:
                    valid_dates.append(start_date)
                    valid_dates.append(end_date)

        return valid_dates

    def get_code(self):
        currency_code = None
        while currency_code is None:
            currency_code = self.validate_code(input('Введіть код валюти (наприклад, USD): '))

        return currency_code

    def get_exchange_rates_today(self):
        currency_code = self.get_code()
        exchange_rate = self.get_exchange_rate(self.today.strftime('%Y%m%d'), currency_code)
        if exchange_rate:
            print(f'\nКурс {currency_code.upper()} на {self.today}: '
                  f'1 {currency_code.upper()} = {exchange_rate}')

    def get_exchange_rates_for_date_input(self):
        dates = self.get_dates()
        currency_code = self.get_code()

        if len(dates) == 1:
            date = dates[0]
            exchange_rate = self.get_exchange_rate(date.strftime('%Y%m%d'), currency_code)
            if exchange_rate:
                print(f'\nКурс {currency_code.upper()} на {date.strftime("%Y-%m-%d")}: '
                      f'1 {currency_code.upper()} = {exchange_rate}')
            else:
                print(f'\nІнформація про курс {currency_code} на вказану дату відсутня')
        elif len(dates) == 2:
            start_date = dates[0]
            end_date = dates[1]

            exchange_rates = self.get_exchange_rates(start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'),
                                                     currency_code)
            if exchange_rates:
                self.show_exchange_rates(start_date, end_date, currency_code, exchange_rates)
        else:
            print('\nНевірний формат дати. Введіть у форматі "рік-місяць-день" або "початкова_дата кінцева_дата"')

    @staticmethod
    def print_menu():
        print('\nМеню:')
        print('1. Переглянути доступні валюти')
        print('2. Отримати курс валюти на сьогодні')
        print('3. Отримати курс валюти за датою')
        print('4. Вийти')

    def start(self):
        while True:
            self.print_menu()
            choice = input('Виберіть опцію (1/2/3/4): ')

            match choice:
                case '1':
                    self.show_available_currencies()
                case '2':
                    self.get_exchange_rates_today()
                case '3':
                    self.get_exchange_rates_for_date_input()
                case '4':
                    print("\nДо побачення!")
                    return
                case _:
                    print('\nНевірний вибір. Спробуйте ще раз.')


if __name__ == "__main__":
    ExchangeRates().start()
