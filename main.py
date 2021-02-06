import os
import time

import pandas as pd

from scraping_var_functions import base_url, mm_params, position
from scraping_var_functions import return_filename, convert_datatypes_technical, trend_template_filter
from scraping_var_functions import return_single_table_from_finviz


def scrap_TT():

# Check if the program has been run today
    filename = return_filename()
    if os.path.isfile(filename):
        return pd.read_csv(filename, index_col='Ticker')

# Check amount of stocks and determine the pages required to click through finviz
    trial = return_single_table_from_finviz(position, base_url, mm_params, True)
    total = trial[1]
    results = trial[0]
    print(total)

#    total = 60
#   uncomment total for testing purposes

# Loop through finviz scrapping the entire list
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



