import pandas as pd
from scraper import Scraper

# Configuration parameters for fetching currency data from the NBP API
base_url = 'http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/last/{topCount}/'
table = 'A'  # Table identifier for currency rates
days = 90  # Number of days for data retrieval

currency_scraper = Scraper()  # Instantiating the Scraper class for currency data manipulation


def data_analysis():
    # Loading selected currency data from a CSV file and initializing a dictionary for statistics
    selected_df = pd.read_csv('selected_currency_data.csv')
    stats_dict = {}  # Dictionary to store basic statistics for numeric columns

    # Calculating basic statistics for numeric columns (excluding 'Date') in the selected currency data
    # and storing them in the stats_dict dictionary
    for column in selected_df.columns:
        if column != 'Date':
            column_values = selected_df[column]
            if pd.api.types.is_numeric_dtype(column_values):
                avg_value = column_values.mean()
                median_value = column_values.median()
                min_value = column_values.min()
                max_value = column_values.max()

                stats_dict[column] = [avg_value, median_value, min_value, max_value]

    # Generating and displaying basic statistics for the selected currency data columns
    stats_df = pd.DataFrame(stats_dict, index=['Average rate value', 'Median', 'Minimum', 'Maximum'])
    print(f"\n{stats_df}")


# Retrieving currency data, user selection prompt, and initiating data analysis
currency_scraper.fetch_currency_data(base_url, table, days)  # Fetches currency data
currency_scraper.data_selection()  # Manages user currency selection
data_analysis()  # Performs basic data analysis for selected currencies

