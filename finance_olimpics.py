import retrieve_data
from datetime import date, datetime
from collections import defaultdict
import pandas as pd

path = '/mnt/c/Users/epiph/OneDrive - Universidade de Santiago de Compostela(1)/Locas olimpiadas financieras'
wallets = {
    'WWS':{
        'path': path+'/WWS/WWS.xlsx',
        'short': []
        },
    'NoName': {
        'path': path+'/NoName/NoName.xlsx',
        'short': []
        },
    'Oira': {
        'path': path+'/Oira/Oira.xlsx',
        'short': []
        },
    'CAPM_Sampayo': {
        'path': path+'/CAPM_Sampayo/CAPM_Sampayo.xlsx',
        'short': ['VIS.MC', 'IAG.MC']
        },
    'Massive_dynamic': {
        'path': path+'/Massive_dynamic/Massive_dynamic.xlsx',
        'short': ['REP.MC']
        }
    #'Andres': {
    #    'path': path+'/Andres/Andres.xlsx',
    #    'short': []
    #}
    }

to ='2020-03-30'#date.today().isoformat()

def wallet_actualization(df, to, wallet, historico):
    cartera = df.columns[df.loc[df.index[-1]]!=0][: len(df.columns) - 5]
    since = format_date(df.index[-1])
    weights = []
    positions = []
    for col in cartera:
        weights.append(df[col][df.index[-1]]/df['total'][df.index[-1]])
        positions.append(col in wallet['short'])
    cartera_join = ' '.join(cartera)
    res = retrieve_data.simulateInvestments(cartera=cartera_join,
                                            weights=weights,
                                            since = since,
                                            to = str(to),
                                            investment=df['total'][df.index[-1]],
                                            positions=positions)
    stocks = []
    for i in range(len(cartera)):
        if cartera[i] in historico.columns:
            if positions[i]:
                stocks.append((df[cartera[i]][df.index[-1]]/historico[cartera[i]][to])*historico[cartera[i]][since])
            else:
                stocks.append((df[cartera[i]][df.index[-1]]/historico[cartera[i]][since])*historico[cartera[i]][to])
        else:
            stocks.append(res.report[cartera[i]])
    df.loc[to] = stocks+[sum(stocks), 
                         sum(stocks)-df.loc[since]['total'], 
                         sum(stocks)-10000,
                         (sum(stocks)-df.loc[since]['total'])/df.loc[since]['total'],
                         (sum(stocks)-10000)/10000]
    return(df)
    
def format_date(date):
    date = str(date)
    date = date.split(' ')[0]
    return(date)

def report_actualization(wallets, to, path, historico):
    toret = {}
    for wallet in wallets.keys():
        df = pd.read_excel(wallets[wallet]['path'], index_col='date')
        res = wallet_actualization(df, to, wallets[wallet], historico)
        res.to_excel(path+'/last_day_backup/'+wallet+'.xlsx')
        res.to_excel(path+'/backup/'+wallet+to+'.xlsx')
        toret[wallet] = res
    return(toret)

def send_results(dict, wallets, df, path):
    for wallet in wallets.keys():
        dict[wallet].to_excel(wallets[wallet]['path'])
        df.to_excel(path+'/'+wallet+'/'+'ranking_general.xlsx')
        df.to_excel((path+'/backup/ranking'+to+'.xlsx')
        
def get_ranking(dict, wallets, to):
    toret = defaultdict(list)
    for wallet in wallets.keys():
        toret['team'].append(wallet)
        toret['wallet value'].append(dict[wallet]['total'][to])
        toret['team profit'].append(dict[wallet]['general profit'][to])
        toret['team yield'].append(dict[wallet]['general yield'][to])
    toret = pd.DataFrame(toret)
    toret = toret.sort_values(by=['wallet value'], ascending=False)
    toret['Position'] = range(1,len(toret.index)+1)
    toret.set_index('Position', drop=True, inplace=True)
    return(toret)

def actualize_historic():
    historico = pd.read_excel(path+'/backup/historico.xlsx', index_col='date')
    hist = ' '.join(historico.columns)
    res= retrieve_data.retrieveData(tickers=hist,
                               period='1y',
                               interval='1d').data 
    row = [float(res[(stock, 'Close')]) for stock in historico.columns]
    historico.loc[to] = row
    historico.to_excel(path+'/backup/historico.xlsx')
    return(historico)


historico = actualize_historic()
result = report_actualization(wallets, to, path, historico)


rank = get_ranking(dict=result, wallets=wallets, to=to)
rank


send_results(dict=result,
             wallets=wallets,
             df=rank,
             path=path)
