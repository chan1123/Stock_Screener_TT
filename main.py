import requests, os, time
import pandas as pd
import numpy as np
from scraping_headers import finviz_headers, base_url, mm_params, position, technical_numeric_list, technical_percentage_list
from scraping_misc import parse_total_stocks, return_filename, convert_datatypes_technical, trend_template_filter
from scraping_misc import return_single_table_from_finviz
from bs4 import BeautifulSoup


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
    filtered = trend_template_filter(convert_datatypes_technical(results))
    filtered.to_csv(filename)
    return filtered

df = scrap_TT()
print(df)
print(df.dtypes)



