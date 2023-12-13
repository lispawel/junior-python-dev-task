# junior-python-dev-task
This code is for a recruitment task for Junior Python Dev position.


# To do:

### Fetching Currency Data:

- Utilizing the website https://api.nbp.pl/ and Python, retrieve exchange rates for EUR/PLN, USD/PLN, and CHF/PLN for the last 90 days.
- Save this data in separate columns. Additionally, create two more columns containing the EUR/USD and CHF/USD rates, calculated based on the retrieved data.

### Data Selection:

- Allow the user to input the name of the currency pairs they wish to access information for. Ideally, enable the user to specify multiple currency pairs.
- Filter the data to only include rows relevant to the chosen currency pairs.

### Saving Data:

- Save all the previously mentioned data (dates and rates for five pairs) into a CSV file named "all_currency_data.csv".
- Develop a function to permit the saving of only the user-selected currency pairs to a CSV file named "selected_currency_data.csv".
    - The CSV should retain the columns from the original file but only for the currencies selected by the user.
    - Store the filtered data in the CSV file.

### User Interaction:

- After saving the data, display a confirmation message such as "Data for [Currency] has been saved!"

### Error Handling:

- Create and implement appropriate error handling mechanisms for potential issues that might arise during the execution of the script. Ensure that the user is informed in a user-friendly manner about any errors that occur.

### Data Analysis:

- Develop a Python function that calculates and displays the average rate value, median, minimum, and maximum for the selected currency pair.

### Add:

- Implement functionality for the script to run daily at 12:00 PM and automatically save the data to the "all_currency_data.csv" file. Ensure that each script execution overwrites the file only with new entries.

I’ve built this code step by step according to task requirements. Firstly i had to Fetch Currency Data. First thing i did was to import requests module to get data from the api and pandas to save the data into a dataframe which I believe is the best and most flexible way to save data. I set value base_url to the right url template from https://api.nbp.pl/. Then i set these variable values and create a global, empty data frame (df). I did it this way so the url can be dynamically changed at any time. After that i created two functions. The fetch_currency_data() function fills df with data from the last 90 days. To do that i created create_df(code) function that takes code, which is a unique code of the currency, and creates a custom url for given code, fetches the data and cleans it and creates a data frame for each currency code. Then I came back to the fetch_currency_data() function and merged all three data frames together. Lastly i added two new columns to df: 'EUR/USD' and 'CHF/USD' and set index to ‘Date’ column for convenience.

Then i went on to Data Selection task and created data_selection() function. This step asks user to input desired currency pairs which also triggers correct_input(user_input) function that triggers itself until user inputs a valid answer. After validating user input it displays selected data and asks user if he/she wants to save the data. If yes it saves it to "selected_currency_data.csv" and informing user that the desired data has been saved. In any other case it asks again for selecting desired currency pairs. This step also completes Saving Data, User Interaction and Error Handling.

Then i did Data Analysis by adding data_analysis() function. For every currency selected by user it calculates average rate value, median, minimum, and maximum and displays it in a table. 

Then, I needed to add functionality for the script to run daily at 12:00 PM and automatically save the data to the "all_currency_data.csv" file. To do that I created new add_new_data()
  function which is triggered daily at 12:00 PM. What it does is saves current date to string and checks if this date already has currency info in "all_currency_data.csv”. If not then that means it is the newest data since the While loop runs daily, and gets the row for that date from df. Since df displays alst 90 days the only difference between df and what is in file is the last and first row, so I get the last nad overwrite the file only with new entry. I could also do the same as i did for 90 day data but instead do it for las day but it was easier this way since I already had everything I need (df and fetch_currency_data()) in my code to complete this task. 
