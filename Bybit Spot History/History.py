import pandas as pd
import os
from datetime import date, timedelta
import requests
import time

btc_index=[]
btc_open=[]
btc_high=[]
btc_low=[]
btc_close=[]

def download_day(pair,date,period):
    print(date)
    url = "https://public.bybit.com/spot_index/" + pair + "/"+ pair + str(date) + "_index_price.csv.gz"
    r = requests.get(url, allow_redirects=True)

    open('DATA', 'wb').write(r.content)
    data = pd.read_csv('DATA', nrows=1441, compression='gzip')
    
    # Fill in the missing data
    if len(data) < 1440:  
        print("Repaired Missing Data")
        missing_data=pd.DataFrame()
        filler_index = []
        filler_start_at = []
        filler_open = []
        filler_high = []
        filler_low = []
        filler_close = []
        for i in range(1440-len(data)):
            filler_index.append(len(data)+i)
            filler_start_at.append(data['start_at'][len(data)-1]+i*60)
            filler_open.append(data['open'][len(data)-1])
            filler_high.append(data['high'][len(data)-1])
            filler_low.append(data['low'][len(data)-1])
            filler_close.append(data['close'][len(data)-1])
        
        missing_data=pd.DataFrame({'start_at': filler_start_at, 
        'open' : filler_open, 
        'high' : filler_high, 
        'low' : filler_low, 
        'close' : filler_close}, 
        index=filler_index)
        data = pd.concat([data,missing_data])

    if (period == 1):
        btc_index.append(data['start_at'])
        btc_open.append(data['close'])
        btc_high.append(data['high'])
        btc_low.append(data['low'])
        btc_close.append(data['open'])
    else:    
        # Calculate Period Data from minute data
        for i in range(period, 1440+period, period):
            btc_index.append(data['start_at'][i-period])
            btc_open.append(data['close'][i-period])
            btc_high.append(max(data['high'][i-period:i-1]))
            btc_low.append(min(data['low'][i-period:i-1]))
            btc_close.append(data['open'][i-1])

def download_history(pair,start_year, start_month, start_day, period):
    start = (time.time_ns() + 500000) // 1000000
    current_date = date(start_year, start_month, start_day) - timedelta(1)
    end_date = date.today() - timedelta(1)
    delta = timedelta(days=1)

    # Run this for each day
    while current_date < end_date:
        current_date += delta
        download_day(pair,current_date,period)

    os.remove('DATA')     

    # Compile List Data into a Dataframe
    df = pd.DataFrame({'time' : btc_index, 'open' : btc_open, 'high' : btc_high, 'low' : btc_low, 'close' : btc_close})

    # Store Dataframe as a CSV file
    df.to_csv('history.csv', index=False)

    end = (time.time_ns() + 500000) // 1000000
    print(f"\nDownloaded History in {(end - start)/1000} seconds") 

download_history("BTCUSD", 2019, 1, 1, 240)

