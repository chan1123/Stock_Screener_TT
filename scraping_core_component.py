from scraping_headers import my_headers
import requests
from bs4 import BeautifulSoup
import pandas as pd

def return_single_table_from_finviz(table_pos, base_url, parameters, total_stocks=False):
    """
    Submit requests to finviz and scrap only one stock table
    """

    r = requests.get(url=base_url,
                     params=parameters,
                     headers=my_headers)

    html_contents = r.text
    html_soup = BeautifulSoup(html_contents, 'html.parser')

    dfs = pd.read_html(html_contents)

    if True == total_stocks:
        return dfs[table_pos], int(dfs[table_pos - 1].iloc[0, 0].split(' ')[1])
    return dfs[table_pos]

def convert_datatypes_technical(df):
    """
    Return the cleaned dataframe
    """

    # Convert columns from object type to numeric type
    numeric_list = ['Beta', 'ATR', 'RSI', 'Price']
    df[numeric_list] = df[numeric_list].apply(pd.to_numeric, errors='coerce')

    percentage_convert = ['SMA20',
                          'SMA50',
                          'SMA200',
                          '52W High',
                          '52W Low',
                          'from Open',
                          'Gap']

    for item in percentage_convert:
        df[item] = (pd.to_numeric(df[item].replace("-", "100000").str.strip('%'))
                    .div(100).replace(1000.000, np.NaN))

    del df['Change']
    del df['Volume']

    return df


def trend_template_filter(df):
    """
    Filter for Price > SMA50 > SMA200
    PX >= 1.25(52-week low)
    PX >= 0.75(52-week high)
    """

    condition_1 = df['SMA50'] < df['SMA200']
    condition_2 = df['SMA50'] > 0
    condition_3 = df['SMA200'] > 0
    condition_4 = df['52W High'] >= -0.25
    condition_5 = df['52W Low'] >= 0.25

    return df[condition_1 & condition_2 & condition_3 & condition_4 & condition_5]