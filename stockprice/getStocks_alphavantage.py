import requests
import re
import json
from datetime import date

symbols = ['f','anf','ge','intc']

def retrieve_highs():
    current_date = str(date.today())
    print("Current Date: "+current_date)
    url="https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
    for stock in symbols:
        #print(url+stock+"&apikey=7V5RNT4HHZAP6FM6")
        response = requests.get(url+stock+"&apikey=7V5RNT4HHZAP6FM6") # gets the HTTP response code.
        #print(response)
        jsonData  = response.json() if response and response.status_code==200 else None # Convert the response to json data if respoonse code is 200.
        #print(jsonData)
        if(jsonData):
            '''print(jsonData['Meta Data']['2. Symbol'])
            print(jsonData["Time Series (Daily)"][current_date])
            '''
            stock_ticker = (str)(jsonData['Meta Data']['2. Symbol']).upper()
            open_price = (float)(jsonData["Time Series (Daily)"][current_date]['1. open'])
            high_price = (float)(jsonData["Time Series (Daily)"][current_date]['2. high'])
            low_price = (float)(jsonData["Time Series (Daily)"][current_date]['3. low'])
            close_price = (float)(jsonData["Time Series (Daily)"][current_date]['4. close'])
            stock_volume = (float)(jsonData["Time Series (Daily)"][current_date]['5. volume'])

            print("Stock: {0} Open: {1} High: {2} Low: {3} Closing: {4} Volume: {5}".format(stock_ticker,open_price,high_price,low_price,close_price,stock_volume))
    

def main():
    retrieve_highs()
main()