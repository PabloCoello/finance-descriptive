import retrieve_data
from datetime import date, datetime
from collections import defaultdict
import pandas as pd

path = '/mnt/c/Users/epiph/OneDrive - Universidade de Santiago de Compostela(1)/Locas olimpiadas financieras'
wallets = {
    'WWS': path+'/WWS/WWS.xlsx'
    #'eco2': path+'/team2/team2.xlsx',
    #'Juan': path+'/team3/team3.xlsx',
    #'Maria_y_Clara': path+'/team4/team4.xlsx',
    #'Ourense':path+'/team5/team5.xlsx',
    }

to =date.today().isoformat()

def wallet_actualization(df, to):
    cartera = df.columns[df.loc[df.index[-1]]!=0][: len(df.columns) - 5]
    since = format_date(df.index[-1])
    weights = []
    for col in cartera:
        weights.append(df[col][df.index[-1]]/df['total'][df.index[-1]])
    cartera_join = ' '.join(cartera)
    res = retrieve_data.simulateInvestments(cartera=cartera_join,
                                            weights=weights,
                                            since = since,
                                            to = str(to),
                                            investment=df['total'][df.index[-1]])
    stocks = []
    for stock in cartera:
        stocks.append(res.report[stock])
    df.loc[to] = stocks+[sum(stocks), 
                         sum(stocks)-df.loc[since]['total'], 
                         sum(stocks)-10000,
                         (sum(stocks)-df.loc[since]['total'])/df.loc[since]['total'],
                         (sum(stocks)-10000)/10000]
    return(df)
    

def report_actualization(wallets, to, path):
    for wallet in wallets.keys():
        df = pd.read_excel(wallets[wallet], index_col='date')
        res = wallet_actualization(df, to)
        res.to_excel(path+'/'+wallet+'.xlsx')
    return(res)

def format_date(date):
    date = str(date)
    date = date.split(' ')[0]
    return(date)

result = report_actualization(wallets, to, path)
