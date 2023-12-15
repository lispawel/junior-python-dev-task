from scraper import Scraper
import schedule
import time

currency_scraper = Scraper()  # Initializes the Scraper class

schedule.every().day.at("12:00").do(currency_scraper.add_new_data)  # Schedules new data addition at 12:00 daily

while True:
    schedule.run_pending()  # Runs pending scheduled tasks
    time.sleep(60)  # Pauses the loop for 60 seconds
