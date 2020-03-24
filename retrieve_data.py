import yfinance as yf
from collections import defaultdict
import pandas as pd
from datetime import date, datetime

class retrieveData():
    def __init__(self, tickers, period, interval):
        ticks = tickers.split(' ')
        self.data = yf.download(  # or pdr.get_data_yahoo(...
                # tickers list or string as well
                tickers = tickers,

                # use "period" instead of start/end
                # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                # (optional, default is '1mo')
                period = period,

                # fetch data by interval (including intraday if period < 60 days)
                # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                # (optional, default is '1d')
                interval = interval,

                # group by ticker (to access via data['SPY'])
                # (optional, default is 'column')
                group_by = 'ticker',

                # adjust all OHLC automatically
                # (optional, default is False)
                auto_adjust = True,

                # download pre/post regular market hours data
                # (optional, default is False)
                prepost = True,

                # use threads for mass downloading? (True/False/Integer)
                # (optional, default is True)
                threads = True,

                # proxy URL scheme use use when downloading?
                # (optional, default is None)
                proxy = None
            )
        self.data = self.get_df_variable(tickers=ticks, 
                                         function=self.calculate_yield)
        self.data = self.get_df_variable(tickers=ticks, 
                                         function=self.calculate_volatility)
    
    def calculate_yield(self, col):
        new_col = (col[0], col[1] + ' yield')
        yields = []
        for i in range(len(self.data.index)):
            if i == 0:
                yields.append(None)
            else:
                yields.append(float((self.data[col][i]-
                               self.data[col][i-1])/
                               self.data[col][i-1]))
        self.data[new_col] = yields
        return(self.data)
    
    def calculate_volatility(self, col):
        new_col = (col[0], col[1] + ' volatility')
        volat = []
        for i in range(len(self.data.index)):
            if i == 0:
                volat.append(None)
            else:
                volat.append(float(((self.data[col][i]-
                               self.data[col][i-1])/
                               self.data[col][i-1])**2))
        self.data[new_col] = volat
        return(self.data)
    
    def get_df_variable(self, tickers, function):
        features = ['Open', 'High', 'Low', 'Close']
        for tick in tickers:
            index = [(tick, feat) for feat in features]
            for col in index:
                self.data = function(col=col) 
        return(self.data)

class plotisPlot():
    def get_xs_plot(self, df, var):
        df.xs(var, axis=1, level=1).plot(figsize=(12,5))

class simulateInvestments(retrieveData):
    def __init__(self, cartera, weights, since, to, investment):
        delta = date.today() - datetime.strptime(since, '%Y-%m-%d')
        data = retrieveData.__init__(tickers=cartera, 
                                     period=self.get_retrieve_period(since),
                                     interval='1d')
        ticks = cartera.split(' ')
    
    def get_retrieve_period(self, since):
        dia = since.split('-')
        since = date(int(dia[0]),
                     int(dia[1]),
                     int(dia[2]))
        delta = date.today() - since
        toret = (delta.days//365) + 1
        return(toret)
    
    def get_actual_value(self, ticks, weights, investment, data, since, to):
        returns = {}
        for i in range(len(ticks)):
            col = (ticks[i], 'Close')
            since_price = data[col][since]
            to_price = data[col][to]
            invest = investment/weights[i]
            returns[ticks[i]] = (invest/since_price)*to_price
        return(returns)


r = retrieveData(tickers="MEL.MC AMS.MC AENA.MC",
                 period="1y",
                 interval="1d")
df = r.data
plt = plotisPlot()
plt.get_xs_plot(df, 'Close yield')
