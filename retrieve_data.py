import yfinance as yf
period = ['2019-01-01', '2019-12-31']
data = yf.download("^IBEX", start=period[0], end=period[1])
data['Open'].plot()
