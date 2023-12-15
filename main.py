import requests
import pandas as pd
from datetime import datetime
import time
from scraper import Scraper

base_url = 'http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/last/{topCount}/'
table = 'A'
currency_codes = ['EUR', 'USD', 'CHF']
days = 90

df = pd.DataFrame()
currency_scraper = Scraper()


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

    stats_df = pd.DataFrame(stats_dict, index=['Average rate value', 'Median', 'Minimum', 'Maximum'])
    print(f"\n{stats_df}")


currency_scraper.fetch_currency_data(base_url, table, days)
currency_scraper.data_selection()
data_analysis()

while True:
    current_time = datetime.now()
    if current_time.hour == 12 and current_time.minute == 0:
        currency_scraper.add_new_data()
    time.sleep(60)
