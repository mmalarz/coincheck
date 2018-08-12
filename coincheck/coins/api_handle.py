import bs4 as bs
import datetime as dt
import pandas as pd
import requests


# gets data about coin from given api

def get_data_by_api_url(api_url):
    try:
        context = requests.get(api_url).json()
    except Exception as e:
        print(e)
        context = {}

    return context


# gets monthly data from coinmarketcap.com or can convert all historical data of coin to html file

def get_historical_data(coin, get_html=False):
    url = 'https://coinmarketcap.com/currencies/{}/historical-data/'.format(coin)

    if get_html:
        start = '20130428'  # start parameter - constant starting date for all coins historical data from coinmarketcap.com
        end = dt.datetime.now()
        end = end.strftime('%Y%m%d')
        url = 'https://coinmarketcap.com/currencies/{}/historical-data/?start={}&end={}'.format(coin, start, end)

    try:
        html = requests.get(url)
    except ConnectionError as e:
        print(e)
        return None

    soup = bs.BeautifulSoup(html.content, 'lxml')
    table = soup.find('table', {'class': 'table'})
    data = []

    for row in table.findAll('tr'):
        values = []
        for th in row:
            if th.string != '\n':  # do not allow newline characters be added to list
                values.append(th.string)
        data.append(values)

    if get_html:
        df = pd.DataFrame(data[1:], columns=data[0])
        df.set_index('Date', inplace=True)
        df.to_html('{}.html'.format(coin))
        return None

    return data
