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
        response = requests.get(url+stock+"&apikey=7V5RNT4HHZAP6FM6")
        print(response)
        jsonData  = response.json() if response and response.status_code==200 else None
        print(jsonData)
        if(jsonData):
            print(jsonData["Time Series (Daily)"][current_date])
        
    

def main():
    retrieve_highs()
main()