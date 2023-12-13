import requests
import pandas as pd
from datetime import datetime
import time
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.offline as pyo

base_url = 'http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/last/{topCount}/'

table = 'A'
currency_codes = ['EUR', 'USD', 'CHF']
days = 90

df = pd.DataFrame()


def create_df(code):
    url = base_url.format(table=table, code=code, topCount=days)
    response = requests.get(url)
    data = response.json()
    code_df = pd.DataFrame(data['rates'])
    code_df = code_df.rename(columns={'mid': f'{code}/PLN', 'effectiveDate': 'Date'})
    code_df = code_df.drop('no', axis=1)
    return code_df


def fetch_currency_data():
    global df
    eur_df = create_df('EUR')
    usd_df = create_df('USD')
    chf_df = create_df('CHF')
    df = eur_df.merge(usd_df, how='outer').merge(chf_df, how='outer')
    df['EUR/USD'] = round(df['EUR/PLN'] / df['USD/PLN'], 4)
    df['CHF/USD'] = round(df['CHF/PLN'] / df['USD/PLN'], 4)
    df.set_index('Date', inplace=True)
    # df = df.sort_index(ascending=False)
    # print(df.head())


def data_selection():
    user_input = input("Enter currency pairs separated by space: ").split()
    currencies = correct_input(user_input)
    currencies_upper = [pair.upper() for pair in currencies]
    filtered_data = df[currencies_upper]
    print(filtered_data.sort_index(ascending=False).head())
    save_confirmation = input("Do you want to save selected data (Y/N): ")
    if save_confirmation.lower() == 'y':
        filtered_data.to_csv("selected_currency_data.csv", index=True)
        if len(currencies_upper) > 1:
            formatted_currencies = ', '.join(currencies_upper)
            print(f"Data for {formatted_currencies} have been saved!")
        else:
            print(f"Data for {currencies_upper[0]} has been saved!")
    if save_confirmation.lower() == 'n':
        data_selection()


def correct_input(user_input):
    if len(user_input) == 0:
        new_input = input("Please enter currency pairs separated by space: ").split()
        return correct_input(new_input)
    for currency in user_input:
        if currency.upper() not in df.columns:
            new_input = input(f"There is no such currency as '{currency}'. "
                              f"Please enter available currency pairs separated by space: ").split()
            return correct_input(new_input)
    return user_input


def data_analysis():
    selected_df = pd.read_csv('selected_currency_data.csv')
    stats_dict = {}

    for column in selected_df.columns:
        if column != 'Date':
            column_values = selected_df[column]
            if pd.api.types.is_numeric_dtype(column_values):
                avg_value = column_values.mean()
                median_value = column_values.median()
                min_value = column_values.min()
                max_value = column_values.max()

                stats_dict[column] = [avg_value, median_value, min_value, max_value]

                # print(f"Statistics for column '{column}':")
                # print(f"Average rate value: {avg_value}")
                # print(f"Median: {median_value}")
                # print(f"Minimum: {min_value}")
                # print(f"Maximum: {max_value}")

    stats_df = pd.DataFrame(stats_dict, index=['Average rate value', 'Median', 'Minimum', 'Maximum'])
    print(stats_df)


def add_new_data():
    date_today = str(datetime.now()).split(' ')[0]
    latest_data = pd.read_csv('all_currency_data.csv')
    if date_today not in latest_data['Date'].values:
        latest_row = pd.DataFrame(df.loc[date_today])
        latest_row_transposed = latest_row.transpose()
        latest_row_transposed.to_csv('all_currency_data.csv', mode='a', header=False)

        print(latest_row_transposed)


fetch_currency_data()
df.to_csv("all_currency_data.csv", index=True)
data_selection()
data_analysis()


while True:
    current_time = datetime.now()
    if current_time.hour == 12 and current_time.minute == 0:
        add_new_data()
    time.sleep(60)
