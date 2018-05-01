import re
import urllib
import urllib.request
import json

symbols = ['f','ANF','GE','INTC']

def get_data():
    data = []
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
    for s in symbols:
        url = url+s+"&apikey=7V5RNT4HHZAP6FM6"
    f = urllib.request.urlopen(url).read()
    #print(f)
    j = json.loads(f)
    print("MetaData "+j['Meta Data'[0]])
def main():
    get_data()

main()