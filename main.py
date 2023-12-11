import requests
import pandas as pd

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
    df['EUR/USD'] = df['EUR/PLN'] / df['USD/PLN']
    df['CHF/USD'] = df['CHF/PLN'] / df['USD/PLN']
    df.set_index('Date', inplace=True)
    print(df.head())


fetch_currency_data()
user_input = input("Enter currency pairs separated by space: ").split()
currencies_upper = [pair.upper() for pair in user_input]
filtered_data = df[currencies_upper]
print(filtered_data)
