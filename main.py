import requests, os, time
import pandas as pd
import numpy as np
from scraping_headers import finviz_headers, base_url, mm_params, position, technical_numeric_list, technical_percentage_list
from scraping_misc import parse_total_stocks, return_filename
from bs4 import BeautifulSoup

def return_single_table_from_finviz(position, base_url, parameters, show_stocks=False):
    """
    Submit requests to finviz and scrap only one stock table
    """
    r = requests.get(url=base_url,
                     params=parameters,
                     headers=finviz_headers)

    dfs = pd.read_html(r.text)
    finviz_headers['Referer'] = r.url

    if True == show_stocks:
        total = parse_total_stocks(dfs[position-1])
        return dfs[position], total
    return dfs[position]

def scrap_TT():

    filename = return_filename()
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col='Ticker')

    trial = return_single_table_from_finviz(position, base_url, mm_params, True)
    total = trial[1]

    results = trial[0]
    print(total)
    total = 60

    for _ in list(range(21, total, 20)):
        mm_params['r'] = _
        new_frame = return_single_table_from_finviz(position, base_url, mm_params)
        results = results.append(new_frame)

        time.sleep(4)
        print(_, 'is done')

    return convert_datatypes_technical(results)

def convert_datatypes_technical(df):
    """
    Return the cleaned dataframe
    """
    df.columns = df.iloc[0]
    df.drop(index=[0], inplace=True)
    df.set_index('Ticker', inplace=True)
    del df ['No.']

    # Convert columns from object type to numeric type

    df[technical_numeric_list] = df[technical_numeric_list].apply(pd.to_numeric, errors='coerce')

    for item in technical_percentage_list:
        df[item] = (pd.to_numeric(df[item].replace("-", "100000").str.strip('%'))
                    .div(100).replace(1000.000, np.NaN))

    del df['Change']
    del df['Volume']

    return df


df = scrap_TT()
print(df)
print(df.dtypes)



