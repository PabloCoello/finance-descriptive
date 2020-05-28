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
        'short': ['VIS.MC']
        },
    'Massive_dynamic': {
        'path': path+'/Massive_dynamic/Massive_dynamic.xlsx',
        'short': ['REP.MC']
        },
    'Andres': {
        'path': path+'/Andres/Andres.xlsx',
        'short': []
    },
    'Goldman_sachs': {
        'path': path+'/Goldman_sachs/Goldman_sachs.xlsx',
        'short': []
    }
    }

to =date.today().isoformat()

def wallet_actualization(df, to, wallet, historico):
    ind = df.index[-1]
    cartera = df.columns[: len(df.columns) - 5]

    since = format_date(ind)
    weights = []
    positions = []
    for col in cartera:
        if df.index.duplicated(keep='first')[-1]:
            weights.append(df[col][ind].iloc[1]/df['total'][ind].iloc[1])
            positions.append(col in wallet['short'])
        else:
            weights.append(df[col][ind]/df['total'][ind])
            positions.append(col in wallet['short'])
            
    cartera_join = ' '.join(cartera)
    
    if df.index.duplicated(keep='first')[-1]:
        res = retrieve_data.simulateInvestments(cartera=cartera_join,
                                                weights=weights,
                                                since = since,
                                                to = str(to),
                                                investment=df['total'][ind].iloc[1],
                                                positions=positions)
    else:
        res = retrieve_data.simulateInvestments(cartera=cartera_join,
                                                weights=weights,
                                                since = since,
                                                to = str(to),
                                                investment=df['total'][ind],
                                                positions=positions)
    stocks = []
    for i in range(len(cartera)):
        if cartera[i] in historico.columns:
            if df.index.duplicated(keep='first')[-1]:
                if positions[i]:
                    stocks.append((df[cartera[i]][ind].iloc[1]/historico[cartera[i]][to])*historico[cartera[i]][since])
                else:
                    stocks.append((df[cartera[i]][ind].iloc[1]/historico[cartera[i]][since])*historico[cartera[i]][to])
            else:
                if positions[i]:
                    stocks.append((df[cartera[i]][ind]/historico[cartera[i]][to])*historico[cartera[i]][since])
                else:
                    stocks.append((df[cartera[i]][ind]/historico[cartera[i]][since])*historico[cartera[i]][to])
        else:
            stocks.append(res.report[cartera[i]])
            
    if df.index.duplicated(keep='first')[-1]:
        array = stocks+[sum(stocks), 
                         sum(stocks)-df.loc[since].iloc[1]['total'], 
                         sum(stocks)-10000,
                         (sum(stocks)-df.loc[since].iloc[1]['total'])/df.loc[since].iloc[1]['total'],
                         (sum(stocks)-10000)/10000]
    else:
        array = stocks+[sum(stocks), 
                         sum(stocks)-df.loc[since]['total'], 
                         sum(stocks)-10000,
                         (sum(stocks)-df.loc[since]['total'])/df.loc[since]['total'],
                         (sum(stocks)-10000)/10000]
    df.loc[to] = array
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
        df.to_excel((path+'/backup/ranking'+to+'.xlsx'))
                    
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
    row = [float(res[(stock, 'Close')][-1]) for stock in historico.columns]
    historico.loc[to] = row
    historico.to_excel(path+'/backup/historico.xlsx')
    return(historico)

def fix_result(df, tick, to, amount):
    cartera = df.columns[: len(df.columns) - 5]
    since = format_date(df.index[-2])
    
    df[tick][to] = amount
    
    stocks = []
    for stock in cartera:
        stocks.append(df[stock][to])
        
    df['total'][to]= sum(stocks)
    df['1 day profit'][to] = sum(stocks)-df['total'][since].iloc[1]
    df['general profit'][to] = sum(stocks)-10000
    df['1 day yield'][to] = (sum(stocks)-df['total'][since].iloc[1])/df['total'][since].iloc[1]
    df['general yield'][to] = (sum(stocks)-10000)/10000
    return(df)

def Insert_row(row_number, df, row_value): 
    row_number = row_number-1
    # Starting value of upper half 
    start_upper = 0
   
    # End value of upper half 
    end_upper = row_number 
   
    # Start value of lower half 
    start_lower = row_number 
   
    # End value of lower half 
    end_lower = df.shape[0] 
   
    # Create a list of upper_half index 
    upper_half = [*range(start_upper, end_upper, 1)] 
   
    # Create a list of lower_half index 
    lower_half = [*range(start_lower, end_lower, 1)] 
   
    # Increment the value of lower half by 1 
    lower_half = [x.__add__(1) for x in lower_half] 
   
    # Combine the two lists 
    index_ = upper_half + lower_half 
   
    # Update the index of the dataframe 
    df.index = index_
   
    # Insert a row at the end 
    df.loc[row_number] = row_value 
    
    # Sort the index labels 
    df = df.sort_index()
    Position = [x+1 for x in df.index]
    df['Position']=Position
    df.reset_index(drop=True)
    df.set_index('Position', inplace=True)
   
    # return the dataframe 
    return(df)


historico = actualize_historic()

result = report_actualization(wallets, to, path, historico)

# Add value manually
result['CAPM_Sampayo'] = fix_result(df=result['CAPM_Sampayo'],
                                     tick='^IBEX',
                                     to=to,
                                     amount=1041.354224)

result['CAPM_Sampayo']
result['Goldman_sachs']
result['Massive_dynamic']
result['NoName']
result['Oira']
result['Andres']
result['WWS']

rank = get_ranking(dict=result, wallets=wallets, to=to)
rank

# Insert row in rank of needed
rank = Insert_row(row_number=5,
                  df=rank,
                  row_value=['Andres',10000,0,0])
result

send_results(dict=result,
             wallets=wallets,
             df=rank,
             path=path)
