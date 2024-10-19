import time
import requests
from collections import defaultdict
import os
import subprocess
# Define your API details
api_url = "https://fcsapi.com/api-v3/forex/candle?symbol=AUD/CAD,AUD/CHF,AUD/NZD,AUD/USD,BHD/CNY,CAD/CHF,EUR/GBP,EUR/TRY,GBP/AUD,JOD/CNY,MAD/USD,OMR/CNY,SAR/CNY,USD/CAD,USD/CHF,USD/CNH,USD/DZD,USD/JPY,USD/PHP,USD/THB,YER/USD,EUR/HUF,USD/CLP,EUR/USD,NZD/JPY,NZD/USD,USD/INR,AED/CNY,EUR/CHF,GBP/JPY,USD/RUB,EUR/RUB,CAD/JPY,EUR/JPY,USD/MYR,CHF/NOK,GBP/USD,USD/BDT,USD/PKR,USD/SGD,AUD/JPY,USD/IDR,CHF/JPY,USD/EGP,LBP/USD,QAR/CNY,USD/ARS,EUR/NZD,TND/USD,USD/BRL,USD/MXN,USD/COP,USD/VND,EUR/JPY,GBP/JPY,AUD/CAD,AUD/CHF,AUD/JPY,AUD/USD,CAD/CHF,CAD/JPY,CHF/JPY,EUR/AUD,EUR/CAD,EUR/CHF,EUR/GBP,GBP/AUD,GBP/CAD,GBP/CHF,GBP/USD,USD/CAD,USD/CHF,USD/JPY,EUR/USD&period=1h&access_key=sUzCi6h6fxyoV2L0DxvFE"  # Replace with your actual API URL
signals = defaultdict(list)
num = 1
api_url_2 = "https://fcsapi.com/api-v3/forex/candle?symbol=AUD/CAD,AUD/CHF,AUD/NZD,AUD/USD,BHD/CNY,CAD/CHF,EUR/GBP,EUR/TRY,GBP/AUD,JOD/CNY,MAD/USD,OMR/CNY,SAR/CNY,USD/CAD,USD/CHF,USD/CNH,USD/DZD,USD/JPY,USD/PHP,USD/THB,YER/USD,EUR/HUF,USD/CLP,EUR/USD,NZD/JPY,NZD/USD,USD/INR,AED/CNY,EUR/CHF,GBP/JPY,USD/RUB,EUR/RUB,CAD/JPY,EUR/JPY,USD/MYR,CHF/NOK,GBP/USD,USD/BDT,USD/PKR,USD/SGD,AUD/JPY,USD/IDR,CHF/JPY,USD/EGP,LBP/USD,QAR/CNY,USD/ARS,EUR/NZD,TND/USD,USD/BRL,USD/MXN,USD/COP,USD/VND,EUR/JPY,GBP/JPY,AUD/CAD,AUD/CHF,AUD/JPY,AUD/USD,CAD/CHF,CAD/JPY,CHF/JPY,EUR/AUD,EUR/CAD,EUR/CHF,EUR/GBP,GBP/AUD,GBP/CAD,GBP/CHF,GBP/USD,USD/CAD,USD/CHF,USD/JPY,EUR/USD&period=1h&access_key=gKaYjW9CeMM08mUfxdAGu"

title = "Check Trade"
content = "Check your trading app"
priority = "high"


def fetch_candlestick_data(num):
    # Make an API call to fetch candlestick data
    if num % 2 == 0:
        response = requests.get(api_url)
    else:
        response = requests.get(api_url_2)
    num += 1
    if num > 100:
        num = 0
    if response.status_code == 200:
        return response.json()["response"]  # Assuming the response is JSON
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def generate_signal(opening_price, closing_price):
    if closing_price > opening_price:
        return "buy"
    elif closing_price < opening_price:
        return "sell"
    else:
        return "hold"

while True:
    data = fetch_candlestick_data(num)
    if data:
        for candle in data:
            opening_price = candle['o']
            closing_price = candle['c']
            currency_pair = candle['s']
            
            signal = generate_signal(opening_price, closing_price)
            signals[currency_pair].append(signal)
            #print(f"Signal for {currency_pair}: {signal}")

            # Check for five consecutive signals for the same currency pair
            if len(signals[currency_pair]) >= 5 and all(s == signal for s in signals[currency_pair][-5:]):
                if signals[currency_pair][-1] == "buy" or signals[currency_pair] == "sell":
                    print(f"Bingo for {currency_pair} {signals[currency_pair][-1]}!")
                    subprocess.run([
                        'termux-notification',
                        '--title', title,
                        '--content', content + " for " + currency_pair,
                        '--priority', priority
                    ])

            # Optional: clear signals list if too long to avoid memory issues
            if len(signals[currency_pair]) > 100:  # Keep the last 100 signals for each pair
                signals[currency_pair] = signals[currency_pair][-100:]

    # Wait for an hour before the next API call
    time.sleep(3600)
