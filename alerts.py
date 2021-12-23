#Python API alert program to alert customers when the given ticker price value deviate more than 1%
import datetime
import json
from statistics import mean
import argparse
import requests

#get the arguments from comand line
parser = argparse.ArgumentParser(description='Runs checks on API')
parser.add_argument('-c', '--currency', metavar='CURRENCY', type=str, default='ALL',
                    help='The currency trading pair, or ALL')
parser.add_argument('-d', '--deviation', metavar='DEVIATION', type=int, default=1,
                    help='percentage threshold for deviation')
args = parser.parse_args()
CURRENCY,DEVIATION = args.currency, args.deviation

#Default currency set to all the symbols
if CURRENCY == 'ALL':
    BASE_URL = "https://api.gemini.com/v1"
    response = requests.get(BASE_URL + "/symbols")
    symbols = response.json()
else:
    symbols = []
    symbols.append(CURRENCY)

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
    now = datetime.datetime.now().isoformat()
    for each_symbol in symbols:
        BASE_URL = "https://api.gemini.com/v2"
        response = requests.get(BASE_URL + "/ticker/" + f'{each_symbol}')
        symbol_data = response.json()
        if response.status_code == 200:
            alert_data['level'] = "INFO"
            alert_data['timestamp'] = now
            alert_data['trading_pair'] = symbol_data['symbol']
            alert_data['data']['last_price'] = round(float(symbol_data['close']),2)
            test_list = symbol_data['changes']
            test_list= [float(i) for i in test_list]
            alert_data['data']['average'] = round(mean(test_list),2)
            alert_data['data']['change'] = round((float(symbol_data['close']) \
                                           - float(symbol_data['open'])),2)
            if abs(alert_data['data']['change']) > 0:
                alert_data['deviation'] = True
            else:
                alert_data['deviation'] = False

            if abs(alert_data['data']['average']) == 0:
                alert_data['data']['sdev'] = 1
            else:
                alert_data['data']['sdev']= round(((float(symbol_data['close'])- \
                   float(symbol_data['open'])) / float(symbol_data['open'])) * 100, 1)

            if abs(alert_data['data']['sdev']) > DEVIATION:
                print(json.dumps(alert_data, indent=4))
        else:
            print(json.dumps(symbol_data, indent=4))

#Driver program
if __name__ == '__main__':
    get_ticker()

