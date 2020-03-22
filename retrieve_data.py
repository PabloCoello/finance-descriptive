import sys
import pandas as pd 
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime, date

def request_data(code, period, frequency):
    my_share = share.Share(code)
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_MONTH,
                                            period,
                                            share.FREQUENCY_TYPE_DAY,
                                            frequency)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)
    return(pd.DataFrame(symbol_data))

def format_timestamp(df):
    df['timestamp'] = (df['timestamp']/1000).apply(datetime.fromtimestamp, inplace=True)
    df['timestamp'] = df['timestamp'].apply(date.isoformat)
    return(df)

df = request_data('^IBEX', 12, 1)
df = format_timestamp(df)