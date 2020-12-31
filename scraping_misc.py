from scraping_headers import finviz_headers, technical_numeric_list, technical_percentage_list
import datetime
import pandas as pd
import numpy as np
import requests

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

def parse_total_stocks(df):
    """
    Parse total stocks from df
    :param df:
    :return: int
    """

    phrase = df.iloc[0,0]
    return int(phrase.split(' ')[1])

def return_filename():
    """
    Return filename of today
    :return: string
    """

    date_time = datetime.datetime.now().strftime("%Y%m%d")
    filename = './Trend_Template/' + date_time + '_TT' + '.csv'
    return filename


def convert_datatypes_technical(df_input):
    """
    Return the cleaned dataframe
    """

    df = df_input.copy(deep=True)

    df.columns = df.iloc[0]
    df.drop(index=[0], inplace=True)
    df.set_index('Ticker', inplace=True)
    del df['No.']

    # Convert columns from object type to numeric type

    df[technical_numeric_list] = df[technical_numeric_list].apply(pd.to_numeric, errors='coerce')

    for item in technical_percentage_list:
        df[item] = (pd.to_numeric(df[item].replace("-", "100000").str.strip('%'))
                    .div(100).replace(1000.000, np.NaN))

    del df['Change']
    del df['Volume']

    return df

def trend_template_filter(df_input):
    """
    Filter for Price > SMA50 > SMA200
    PX >= 1.25(52-week low)
    PX >= 0.75(52-week high)
    """

    df = df_input.copy(deep=True)

    condition_1 = df['SMA50'] < df['SMA200']
    condition_2 = df['SMA50'] > 0
    condition_3 = df['SMA200'] > 0
    condition_4 = df['52W High'] >= -0.25
    condition_5 = df['52W Low'] >= 0.25

    return df[condition_1 & condition_2 & condition_3 & condition_4 & condition_5]


