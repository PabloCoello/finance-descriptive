import retrieve_data
from datetime import date, datetime
from collections import defaultdict

wallets = {
    'eco1':{
        'cartera':"MEL.MC AMS.MC AENA.MC",
        'weights':[0.2,0.4,0.4],
        'since':'2020-03-20',
        'to':'2020-03-27',
        'investment':10000
    },
    'eco2':{
        'cartera':"MEL.MC AMS.MC AENA.MC",
        'weights':[0.2,0.4,0.4],
        'since':'2020-03-20',
        'to':'2020-03-27',
        'investment':10000
    },
    'Juan':{
        'cartera':"MEL.MC AMS.MC AENA.MC",
        'weights':[0.2,0.4,0.4],
        'since':'2020-03-20',
        'to':'2020-03-27',
        'investment':10000
    },
    'Maria_y_Clara':{
        'cartera':"MEL.MC AMS.MC AENA.MC",
        'weights':[0.2,0.4,0.4],
        'since':'2020-03-20',
        'to':'2020-03-27',
        'investment':10000
    },
    'Ourense':{
        'cartera':"MEL.MC AMS.MC AENA.MC",
        'weights':[0.2,0.4,0.4],
        'since':'2020-03-20',
        'to':'2020-03-27',
        'investment':10000
    }
}
str(date.today())
def wallet_actualization(wallet):
    res = retrieve_data.simulateInvestments(cartera=wallet['cartera'],
                                  weights=wallet['weights'],
                                  since = wallet['since'],
                                  to = wallet['to'],
                                  investment=wallet['investment'])
    return(res.report)
    

def report_actualization(wallets):
    toret = defaultdict(list)
    for wallet in wallets.keys():
        res = wallet_actualization(wallets[wallet])
        toret[wallet]=res
    return(toret)

result = report_actualization(wallets)
result.keys()
