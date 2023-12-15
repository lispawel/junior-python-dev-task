import pandas as pd
import requests
from datetime import datetime, timedelta
import os


# Creates a DataFrame with currency exchange rates for a specific code using the provided parameters.
def create_df(code, base_url, table, days):
    url = base_url.format(table=table, code=code, topCount=days)
    response = requests.get(url)
    data = response.json()
    # Creating DataFrame and renaming columns for specific currency code
    code_df = pd.DataFrame(data['rates'])
    code_df = code_df.rename(columns={'mid': f'{code}/PLN', 'effectiveDate': 'Date'})
    code_df = code_df.drop('no', axis=1)
    return code_df


class Scraper:
    def __init__(self):
        self.df = pd.DataFrame()
        self.currency_codes = ['EUR', 'USD', 'CHF']

    def fetch_currency_data(self, base_url, table, days):
        # Fetches data for predefined currency codes and performs data manipulation
        for index, code in enumerate(self.currency_codes):
            if index == 0:
                self.df = create_df(code, base_url, table, days)  # Fetching data for the first code
            else:
                self.df = self.df.merge(create_df(code, base_url, table, days),
                                        how='outer')  # Merging data for other codes

        currency_pairs = [('EUR', 'USD'), ('CHF', 'USD')]
        for base, target in currency_pairs:
            try:
                # Calculates currency pairs and handles KeyError exceptions
                self.df[f'{base}/{target}'] = round(self.df[f'{base}/PLN'] / self.df['USD/PLN'], 4)
            except KeyError:
                print(f"There was an exception for {base}/{target}")  # Handles missing data exceptions

        self.df.set_index('Date', inplace=True)  # Sets 'Date' as DataFrame index
        print(f"{self.df.sort_index(ascending=False).head()}\n")  # Displays sorted DataFrame

        if not os.path.exists('all_currency_data.csv'):
            self.df.to_csv('all_currency_data.csv', index=True)  # Saves DataFrame to CSV if file doesn't exist

    def data_selection(self):
        # Facilitates user input for currency selection and handles data saving based on user confirmation
        user_input = input("Enter currency pairs separated by space: ").split(' ')
        currencies = self.correct_input(user_input)  # Validates and corrects input format
        currencies_upper = [pair.upper() for pair in currencies]  # Converts currencies to uppercase
        filtered_data = self.df[currencies_upper]  # Filters DataFrame based on user-selected currencies

        print(f"\n{filtered_data.sort_index(ascending=False).head()}")
        save_confirmation = input(f"\nDo you want to save selected data (Y/N): ")

        latest_data = pd.read_csv('all_currency_data.csv')
        latest_data.set_index('Date', inplace=True)
        filtered_data = latest_data[currencies_upper]
        if save_confirmation.lower() == 'y':
            filtered_data.to_csv("selected_currency_data.csv", index=True)
            if len(currencies_upper) > 1:
                formatted_currencies = ', '.join(currencies_upper)
                print(f"\nData for {formatted_currencies} has been saved!")
            else:
                print(f"\nData for {currencies_upper[0]} has been saved!")
        elif save_confirmation.lower() == 'n':
            self.data_selection()

    def correct_input(self, user_input):
        # Corrects and validates user input for currency pairs
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
        # Adds new currency data to the existing dataset based on date comparison
        latest_data = pd.read_csv('all_currency_data.csv')
        for delay in range(4):
            previous_date = str(datetime.now().date() - timedelta(days=delay))
            if previous_date in self.df.index.values and previous_date not in latest_data['Date'].values:
                latest_row = pd.DataFrame(self.df.loc[previous_date])
                latest_row_transposed = latest_row.transpose()
                latest_row_transposed.to_csv('all_currency_data.csv', mode='a', header=False)
                print("Added new data!")
