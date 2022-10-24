# Bybit-Spot-History
A Python script that retrieves spot candlestick data from Bybit and saves it to a csv

To download spot data:

call the function: download_history(pair, start_year, start_month, start_day, period)

the function takes 5 arguments:

(string) pair: 

"ADAUSD" 
"BITUSD"
"BTCUSD"
"DOTUSD"
"EOSUSD"
"ETHUSD"
"LTCUSD"
"LUNAUSD"
"MANAUSD"
"SOLUSD"
"XRPUSD"

(int) start_year:
Example: 2019

(int) start_month:
Example: 5

(int) start_day:
Example: 22

(int) period:   Refers to the candlestick timeframe, 1h, 30min, 15min ect...
Supported timeframes: 1, 2, 3, 4, 5, 6, 8, 9, 10... all factors of 1440 are supported
Example: 30

# Note----------------------------#
Bybit only has limited spot data history
refer to https://public.bybit.com/spot_index/ to view available historical data

