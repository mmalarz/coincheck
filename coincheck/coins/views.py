from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from .api_handle import *


def coin_list(request):
    api_url = 'https://api.coinmarketcap.com/v2/ticker/'

    context = {
        'crypto_data': get_data_by_api_url(api_url),
    }
    return render(request, 'coins/coin_list.html', context)


def coin_detail(request, coin_name, coin_id):
    api_url = 'https://api.coinmarketcap.com/v2/ticker/{}/'.format(coin_id)

    context = {
        'picture': 'https://s2.coinmarketcap.com/static/img/coins/32x32/{}.png'.format(coin_id),
        'coin': get_data_by_api_url(api_url),
        'data': get_historical_data(coin_name)[1:],  # not getting first row which is table headers
    }
    return render(request, 'coins/coin_detail.html', context)


def download_csv(request, coin_name):
    get_historical_data(coin_name, get_html=True)
    coin_name = str(coin_name)
    try:
        with open('{}.html'.format(coin_name), 'rb') as html:
            response = HttpResponse(html.read())
            response['content_type'] = 'application/html'
            response['Content-Disposition'] = 'attachment;filename={}.html'.format(coin_name)
            return response
    except FileNotFoundError:
        return HttpResponseNotFound('<h1>File not found</h1>')
