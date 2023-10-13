import requests
from django.shortcuts import render
#from .models import Noticia  # Importe seu modelo de notícias aqui

def obter_noticias_da_bbc():
    # Substitua 'YOUR_API_KEY' pela chave da sua conta na News API
    api_key = '11f9a62b34e0465e867c2b4a400730d5'
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': api_key,
        'sources': 'bbc-news',
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get('articles', [])
        return noticias
    else:
        return []

def obter_noticias_da_cnn():
    # Substitua 'YOUR_API_KEY' pela chave da sua conta na News API
    api_key = '11f9a62b34e0465e867c2b4a400730d5'
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': api_key,
        'sources': 'cnn',
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get('articles', [])
        return noticias
    else:
        return []

def obter_noticias_principais(categorias=[]):
    # Substitua 'YOUR_API_KEY' pela chave da sua conta na News API
    api_key = '11f9a62b34e0465e867c2b4a400730d5'
    url = 'https://newsapi.org/v2/top-headlines?country=us'
    params = {
        'apiKey': api_key,
        'category': ','.join(categorias), 
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get('articles', [])
        return noticias
    else:
        return []

def noticias_principais(request):
    categorias = request.GET.getlist('categoria')
    # Recupere as notícias principais (de todas as fontes)
    noticias_principais = obter_noticias_principais(categorias)

    return render(request, 'noticias/noticias_principais.html', {'noticias_principais': noticias_principais, 'categorias': categorias})

def noticias_bbc(request):
    # Recupere e exiba as notícias da BBC
    bbc_noticias = obter_noticias_da_bbc()
    return render(request, 'noticias/noticias_bbc.html', {'bbc_noticias': bbc_noticias})

def noticias_cnn(request):
    # Recupere e exiba as notícias da CNN
    cnn_noticias = obter_noticias_da_cnn()
    return render(request, 'noticias/noticias_cnn.html', {'cnn_noticias': cnn_noticias})
