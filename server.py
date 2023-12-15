from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from scraper import Scraper
import csv

app = Flask(__name__)
currency_scraper = Scraper()

base_url = 'http://api.nbp.pl/api/exchangerates/rates/{table}/{code}/last/{topCount}/'
table = 'A'
currency_codes = ['EUR', 'USD', 'CHF']
days = 90

currency_scraper.fetch_currency_data(base_url, table, days)
df = currency_scraper.df


@app.route('/')
def display_data():
    try:
        return render_template('display_data.html', table=df.sort_index(ascending=False).head().to_html())
    except FileNotFoundError:
        return "File not found."


@app.route('/save_data', methods=['POST'])
def save_data():
    if request.method == 'POST':
        currency_pairs = request.form.get('currency_input')

        # Sprawdzenie poprawności danych
        error_message = ""
        if not currency_scraper.correct_input(currency_pairs):
            error_message = "Invalid currency pairs. Please enter valid currency pairs."

        with open("selected_currency_data.csv", 'r') as file:
            reader = csv.reader(file)
            col_names = next(reader)[1:]

        if len(col_names) > 1:
            formatted_currencies = ', '.join(col_names)
            message = f"\nData for {formatted_currencies} has been saved!"
        else:
            message = f"\nData for {col_names[0]} has been saved!"

        if error_message:
            return render_template('display_data.html', table=df.sort_index(ascending=False).head().to_html(),
                                   message=error_message)
        else:
            currency_scraper.data_selection(currency_pairs)
            return render_template('display_data.html',
                                   table=df[col_names].sort_index(ascending=False).head().to_html(), message=message)


if __name__ == '__main__':
    app.run(debug=True)
