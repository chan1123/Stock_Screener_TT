
import datetime

def parse_total_stocks(df):
    '''
    Parse total stocks from df
    :param df:
    :return: int
    '''

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


