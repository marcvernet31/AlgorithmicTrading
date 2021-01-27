import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math

# Token ID for IEXCloud sandbox API
# Can be changed to use the non-free version
from token import IEX_CLOUD_API_TOKEN

"""
Equal-Weight S&P500 index fund:
--------------------------------------------------------------------------------
This script accepts the value of a portfolio in USD, and calculates how many
shares of each S&P 500 stock needs to be purchased to get an equal-weight
investment of the index fund.

The obtained data comes from IEXCloud API, but from a free "sandbox" version that
returns random data. In order to get reliable results it's necessary to change the
API token for a licensed one. (https://iexcloud.io/)

Future work:
    - Making the fund market-Capitalization weighted, investig proportionally to
    stock size.
    - Adding the possibility to store the retrieved data, as it is the slowest part
"""

"""
Divide a large list of elements into chunks of size n
"""
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

"""
Connect to the API and retrieve for each stock:
    - Price of shares
    - Market Capitalization
Https call to the API are done in batches of 100 elements for eficiency

returns a pd.DataFrame with the requested information for each stock
"""
def retrieve():
    # List of symbol identifiers of S&P500 stocks
    stocks = pd.read_csv("assets/sp_500_stocks.csv")

    # Initialize DataFrame
    my_columns = ['Ticker', 'Stock Price', 'Market Capitalization', 'Number of shares to buy']
    final_df = pd.DataFrame(columns = my_columns)

    # Retrieve data from the API (using batch retrieving)
    symbol_groups = list(chunks(stocks['Ticker'], 100))
    symbol_strings = []
    for i in range(0, len(symbol_groups)):
        symbol_strings.append(','.join(symbol_groups[i]))

    for symbol_string in symbol_strings:
        batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
        data = requests.get(batch_api_call_url).json()
        for symbol in symbol_string.split(','):
            final_df = final_df.append(
                pd.Series([symbol, data[symbol]['quote']['latestPrice'],
                data[symbol]['quote']['marketCap'], 'N/A'], index = my_columns),
                ignore_index = True)

    return final_df


"""
Collect user input from terminal: Value of portfolio in US$
"""
def userInput():
    portfolio_size = input('Enter the value of your portfolio(USD$): ')
    try:
        val = float(portfolio_size)
    except ValueError:
        print("Error: That's not a number")
        portfolio_size = input('Enter the value of your portfolio(USD$): ')
        val = float(portfolio_size)
    return val

"""
Save a pd.DataFrame as Excel with specific formating
"""
def saveAsExcel(df):
    # Initialize writting object
    writer = pd.ExcelWriter('recomendedTrades.xlsx', engine = 'xlsxwriter')
    df.to_excel(writer, 'Recomended Trades', index = False)

    # Formatting specifications
    background_color = '#0a0a23'
    font_color = '#ffffff'

    string_format = writer.book.add_format({
        #'font_color': font_color,
        #'bg_color': background_color,
        'border':1
    })

    dollar_format = writer.book.add_format({
        'num_format': '$0.00',
        #'font_color': font_color,
        #'bg_color': background_color,
        'border':1
    })

    integer_format = writer.book.add_format({
        'num_format':'0',
        #'font_color': font_color,
        #'bg_color': background_color,
        'border':1
    })

    column_formats = {
    'A': ['Ticker', string_format],
    'B': ['Stock Price', dollar_format],
    'C': ['Marketing Capitalization', dollar_format],
    'D': ['Number of shares to buy', integer_format]
    }

    for column in column_formats.keys():
        writer.sheets['Recomended Trades'].set_column(f'{column}:{column}', 18, column_formats[column][1])
        writer.sheets['Recomended Trades'].write(f'{column}1', column_formats[column][0], column_formats[column][1])
    writer.save()


def main():
    val = userInput()
    df = retrieve()

    position_size = val / len(df.index)
    for i in range(0, len(df.index)):
        df.loc[i, 'Number of shares to buy'] = math.floor(position_size/df.loc[i, 'Stock Price'])

    saveAsExcel(df)
    print("Saved. Data in recomendedTrades.xlsx")

main()
