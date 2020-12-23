finviz_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) \
                  AppleWebKit/537.36 (KHTML, like Gecko) Chrome',
                  'Accept-Language': 'en-gb',
                  'Accept-Encoding': 'deflate',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9, \
                  image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                  'Referer': 'http://www.google.com/'}

base_url = 'https://finviz.com/screener.ashx'

mm_params = {
    'v': 171,
    'f': 'cap_smallover,fa_salesqoq_o5,ind_stocksonly,sh_instown_o10,sh_price_o5,ta_sma200_sb50,ta_sma50_pa',
    'ft': 4
}

position = 16

technical_numeric_list = ['Beta', 'ATR', 'RSI', 'Price']

technical_percentage_list = [
    'SMA20',
    'SMA50',
    'SMA200',
    '52W High',
    '52W Low',
    'from Open',
    'Gap'
]


