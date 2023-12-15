import pandas as pd
import requests
from datetime import datetime


def create_df(code, base_url, table, days):
    url = base_url.format(table=table, code=code, topCount=days)
    response = requests.get(url)
    data = response.json()
    code_df = pd.DataFrame(data['rates'])
    code_df = code_df.rename(columns={'mid': f'{code}/PLN', 'effectiveDate': 'Date'})
    code_df = code_df.drop('no', axis=1)
    return code_df


class Scraper:
    def __init__(self):
        self.df = pd.DataFrame()

    def fetch_currency_data(self, base_url, table, days):
        eur_df = create_df('EUR', base_url, table, days)
        usd_df = create_df('USD', base_url, table, days)
        chf_df = create_df('CHF', base_url, table, days)

        self.df = eur_df.merge(usd_df, how='outer').merge(chf_df, how='outer')
        self.df['EUR/USD'] = round(self.df['EUR/PLN'] / self.df['USD/PLN'], 4)
        self.df['CHF/USD'] = round(self.df['CHF/PLN'] / self.df['USD/PLN'], 4)
        self.df.set_index('Date', inplace=True)
        print(f"{self.df.sort_index(ascending=False).head()}\n")

    def data_selection(self):
        user_input = input("Enter currency pairs separated by space: ").split()
        currencies = self.correct_input(user_input)
        currencies_upper = [pair.upper() for pair in currencies]
        filtered_data = self.df[currencies_upper]

        print(f"\n{filtered_data.sort_index(ascending=False).head()}")
        save_confirmation = input(f"\nDo you want to save selected data (Y/N): ")

        if save_confirmation.lower() == 'y':
            filtered_data.to_csv("selected_currency_data.csv", index=True)
            if len(currencies_upper) > 1:
                formatted_currencies = ', '.join(currencies_upper)
                print(f"\nData for {formatted_currencies} have been saved!")
            else:
                print(f"\nData for {currencies_upper[0]} has been saved!")
        elif save_confirmation.lower() == 'n':
            self.data_selection()

    def correct_input(self, user_input):
        if len(user_input) == 0:
            new_input = input("Please enter currency pairs separated by space: ").split()
            return self.correct_input(new_input)

        for currency in user_input:
            if currency.upper() not in self.df.columns:
                new_input = input(f"There is no such currency as '{currency}'. "
                                  f"Please enter available currency pairs separated by space: ").split()
                return self.correct_input(new_input)

        return user_input

    def add_new_data(self):
        date_today = str(datetime.now()).split(' ')[0]
        latest_data = pd.read_csv('all_currency_data.csv')
        if date_today not in latest_data['Date'].values:
            latest_row = pd.DataFrame(self.df.loc[date_today])
            latest_row_transposed = latest_row.transpose()
            latest_row_transposed.to_csv('all_currency_data.csv', mode='a', header=False)
            print("Added new data!")
