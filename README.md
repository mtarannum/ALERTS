# ALERTS

This python alert program alerts a json log file with ticker data if ticker price deviated more than the input value.


**How to call the program**
$ python alerts.py -h                                                
usage: alerts.py [-h] [-c CURRENCY] [-d DEVIATION]                   
                                                                     
Runs checks on API                                                   
                                                                     
optional arguments:                                                  
  -h, --help            show this help message and exit              
  -c CURRENCY, --currency CURRENCY                                   
                        The currency trading pair, or ALL            
  -d DEVIATION, --deviation DEVIATION                                
                        percentage threshold for deviation       
                        
**Output sample**

$ python alerts.py -c ETHGBP -d 1                           
{                                                           
    "timestamp": "2021-12-22T18:17:55.792233",              
    "level": "INFO",                                        
    "trading_pair": "ETHGBP",                               
    "deviation": true,                                      
    "data": {                                               
        "last_price": 2991.09,                              
        "average": 3023.06,                                 
        "change": 31.97,                                    
        "sdev": 1.1                                         
    }                                                       
}                                                           

**Error sample**
$ python alerts.py -c BCHCUSD -d 1                                 
{                                                                  
    "result": "error",                                             
    "reason": "Bad Request",                                       
    "message": "Supplied value 'BCHCUSD' is not a valid symbol"    
}     
**Requirements needed to run the program**
Following packages needs to installed in python environment to run this program successfully.
pip install datetime
pip install json
pip install statistics
pip install argparse
pip install jq
pip install requests



**Improvements needed in future**
This program can be further improved to called from a monitoring tool like grafana and when the deviation value is reach threshold the output can be send to paging system to alert the customers/users.Also the program can be improved to write the logs to monitoring tool instead of terminal stdout.
