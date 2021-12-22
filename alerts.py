# Python API alert program to alert customers when the given ticker price value deviate more than 1%
import datetime
from statistics import mean
import json
import argparse
import requests

#get the arguments from comand line
parser = argparse.ArgumentParser(description='Runs checks on API')
parser.add_argument('-c', '--currency', metavar='CURRENCY', type=str,
                    help='The currency trading pair, or ALL')
parser.add_argument('-d', '--deviation', metavar='DEVIATION', type=int,
                    help='percentage threshold for deviation')
args = parser.parse_args()
currency=args.currency
deviation=args.deviation

#Default deviation value is set to 1
if deviation is None:
    deviation=1

#Default currency set to all the symbols
if currency in (None, 'ALL'):
    base_url = "https://api.gemini.com/v1"
    response = requests.get(base_url + "/symbols")
    symbols = response.json()
else:
    symbols = []
    symbols.append(currency) 
    
#Define the output variable
alert_data={
  "timestamp": "",
  "level": "",
  "trading_pair": "",
  "deviation": True ,
  "data": {
    "last_price": "",
    "average": "",
    "change": "",
    "sdev": ""
          }
           }
           
# for each ticker, get ticker values from public API and calculate average and deviation
def get_ticker():
    now = datetime.datetime.now().replace(microsecond=4).isoformat()
    for each_symbol in symbols:
        print(each_symbol)
        base_url = "https://api.gemini.com/v2"
        response = requests.get(base_url + "/ticker/" + f'{each_symbol}')
        symbol_data = response.json()
        print(symbol_data)
        if response.status_code == 200:
            alert_data['level'] = "INFO"
            alert_data['timestamp'] = now
            alert_data['trading_pair'] = symbol_data['symbol']
            alert_data['data']['last_price'] = float(symbol_data['close'])
            test_list = symbol_data['changes']
            test_list= [float(i) for i in test_list]
            alert_data['data']['average'] = mean(test_list)
            alert_data['data']['change'] = abs(alert_data['data']['average'] \
                                           - alert_data['data']['last_price'])
            if alert_data['data']['change'] > 0:
                alert_data['deviation'] = True
            else:
                alert_data['deviation'] = False
#             alert_data['data']['sdev'] = stdev(test_list)
            alert_data['data']['sdev']=(alert_data['data']['change'] \
                                        / alert_data['data']['average']) * 100
            if alert_data['data']['sdev'] > deviation:
                print(json.dumps(alert_data, indent=4))
        else:
            print(json.dumps(symbol_data, indent=4))
            
#Driver program
if __name__ == '__main__':
    get_ticker()
