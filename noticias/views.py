import requests
from django.shortcuts import render, redirect
from .models import Comentario
from .forms import ComentarioForm

def adicionar_comentario(request, url_noticia):
    # Encontre a notícia com base na URL (conforme descrito anteriormente)
    noticias = obter_noticias_principais()  # Supondo que esta função obtenha as notícias principais

    # Encontre a notícia correspondente com base no URL
    noticia = None
    for n in noticias:
        if n.get('url') == url_noticia:
            noticia = n
            break

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data['texto']
            Comentario.objects.create(texto=texto, noticia=noticia)
            return redirect('detalhes_noticia', url_noticia=url_noticia)
    else:
        form = ComentarioForm()

    return render(request, 'noticias/comentario_form.html', {'form': form})


def detalhes_noticia(request, url_noticia):
    # Recupere o título e o conteúdo da notícia com base no URL
    # Isso pode ser feito consultando a lista de notícias obtidas da API da News
    # Exemplo de consulta em uma lista de notícias
    noticias = obter_noticias_principais()  # Supondo que esta função obtenha as notícias principais

    # Encontre a notícia correspondente com base no URL
    noticia_principal = None
    for n in noticias:
        if n.get('url') == url_noticia:
            noticia_principal = n
            break
        
    # Adicione lógica para encontrar notícias relacionadas (exemplo: notícias da mesma categoria)
    noticias_relacionadas = []
    for n in noticias:
        if n.get('source.name') == noticia_principal.get('source.name') and n.get('url') != url_noticia:
            noticias_relacionadas.append(n)
            
    noticias_relacionadas = noticias_relacionadas[:3]

    return render(request, 'noticias/detalhes_noticia.html', {'noticia_principal': noticia_principal, 'noticias_relacionadas': noticias_relacionadas})

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
