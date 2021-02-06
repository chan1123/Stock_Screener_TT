# Libraries required

import datetime

import numpy as np
import pandas as pd
import requests

# Variables

# Header used to trick finviz into thinking I am human
finviz_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome',
                  'Accept-Language': 'en-gb',
                  'Accept-Encoding': 'deflate',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, \
                  image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Referer': 'http://www.google.com/'}

# url for scrapping
base_url = 'https://finviz.com/screener.ashx'

# parameters used to filter stocks preliminarily
mm_params = {
    'v': 171,
    'f': 'cap_smallover,fa_salesqoq_o5,ind_stocksonly,sh_instown_o10,sh_price_o5,ta_sma200_sb50,ta_sma50_pa',
    'ft': 4
}

# the 17th table in html
position = 16

# list of numeric values
technical_numeric_list = ['Beta', 'ATR', 'RSI', 'Price']

# list of percentage values
technical_percentage_list = [
    'SMA20',
    'SMA50',
    'SMA200',
    '52W High',
    '52W Low',
    'from Open',
    'Gap'
]


######################################################################
# Functions

def return_single_table_from_finviz(position, base_url, parameters, show_stocks=False):
    """
    Submit requests to finviz and scrap only one stock table
    """
    r = requests.get(url=base_url,
                     params=parameters,
                     headers=finviz_headers)

    dfs = pd.read_html(r.text)
    finviz_headers['Referer'] = r.url

    if show_stocks:
        total = parse_total_stocks(dfs[position - 1])
        return dfs[position], total
    return dfs[position]


def parse_total_stocks(df):
    """
    Parse total stocks from df
    :param df:
    :return: int
    """

    phrase = df.iloc[0, 0]
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
