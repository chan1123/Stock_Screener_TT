import pandas as pd
import numpy as np
import datetime
import time
import requests
from bs4 import BeautifulSoup
import os


# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import pyperclip

def return_single_table_from_finviz(table_pos, base_url, parameters, total_stocks=False):
    """
    Submit requests to finviz and scrap only one stock table
    """
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome',
                  'Accept-Language': 'en-gb',
                  'Accept-Encoding': 'deflate',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, \
                  image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Referer': 'http://www.google.com/'}

    r = requests.get(url=base_url,
                     params=parameters,
                     headers=my_headers)

    html_contents = r.text
    html_soup = BeautifulSoup(html_contents, 'html.parser')

    dfs = pd.read_html(html_contents)

    if True == total_stocks:
        return dfs[table_pos], int(dfs[table_pos - 1].iloc[0, 0].split(' ')[1])
    return dfs[table_pos]


def scrap_all_stocks_TT(finviz_screener=False):
    """
    Scrap all stocks fitting trend template
    Only option is technical
    """

    date_time = datetime.datetime.now().strftime("%Y%m%d")
    filename = './Trend_Template/' + date_time + '_TT' + '.csv'

    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col='Ticker')

    base_url = 'https://finviz.com/screener.ashx'
    if finviz_screener == False:
        finviz_screener = 'cap_smallover,fa_quickratio_o0.5,fa_salesqoq_o5,ind_stocksonly,sh_curvol_o50,sh_price_o7,ta_highlow52w_a20h,ta_sma200_sb50,ta_sma50_pa'

    parameters = {'f': finviz_screener,
                  'v': 171,
                  'ft': 4}
    position = 16

    trial = return_single_table_from_finviz(table_pos=position,
                                            base_url=base_url,
                                            parameters=parameters,
                                            total_stocks=True)
    total = trial[1]
    results = trial[0]
    print(total)

    total = 60
    for _ in list(range(21, total, 20)):
        parameters['r'] = _

        new_frame = return_single_table_from_finviz(table_pos=position,
                                                    base_url=base_url,
                                                    parameters=parameters)

        new_frame.drop(new_frame.index[0], inplace=True)

        results = results.append(new_frame)

        time.sleep(4)
        print(_, 'is done')

    results.columns = results.iloc[0]
    results.drop(index=[0], inplace=True)
    results.set_index('Ticker', inplace=True)
    del results['No.']

    # Saving the stocks to folder

    converted_result = trend_template_filter(convert_datatypes_technical(results))
   # converted_result.to_csv(filename)
    print(converted_result)
    return converted_result


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


scrap_all_stocks_TT()
