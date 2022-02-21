import requests
import pandas
from datetime import datetime as dt
from datetime import timedelta as td
import sys

future_code = '1231'
number_of_results = 30

def get_markets():
    columns = ['name', 'type', 'currency', 'last']
    response = requests.get('https://ftx.com/api/markets')
    if response.ok:
        df = pandas.DataFrame(response.json()['result'])
        df = df.loc[df['quoteCurrency'].isin(['USD', None]) & ~df['name'].str.contains('MOVE')] 
        df['currency'] = df[['underlying', 'baseCurrency']].apply(lambda x: x[0] if x[0] else x[1], axis=1)
        return df[columns]
    else: 
        return None

def get_funding_rates():
    columns = ['future', 'rate']
    start_time = dt.timestamp(dt.now() - td(hours = 1))
    end_time = dt.timestamp(dt.now())
    response = requests.get(f'https://ftx.com/api/funding_rates?start_time={start_time}&end_time={end_time}')
    if response.ok:
        df = pandas.DataFrame(response.json()['result'])[columns]
        return df
    else: 
        return None


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Please provide exactly 1 argument')
    elif sys.argv[1] == 'funding':
        df = get_funding_rates()
        print(df.sort_values(by='rate', key=abs, ascending=[False]).head(number_of_results))
    elif sys.argv[1] == 'diff': 
        df = get_markets()
        df = df.merge(df.loc[df['type'] == 'spot', ['currency', 'last']], how='left', on='currency', suffixes=(None, '_spot_price'))
        df['diff'] = df['last']/df['last_spot_price'] - 1
        df = df.loc[df['name'].str.contains(future_code)] 
        print(df.sort_values(by='diff', key=abs, ascending=[False]).head(number_of_results))
    else:
        print('Argument not recognized')