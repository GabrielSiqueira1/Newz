import requests
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Comentario
from .forms import ComentarioForm
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from dateutil import parser
from django.contrib.auth.views import LoginView
from .forms import CustomLoginForm

API_KEY="11f9a62b34e0465e867c2b4a400730d5"


def obter_ultimas_noticias(request):
    noticias = obter_noticias_principais()
    return JsonResponse({'noticias': noticias})

def resultados_pesquisa(request):
    query = request.GET.get("q")
    noticias = []
    noticias.extend(obter_noticias_principais())
    noticias.extend(obter_noticias_da_bbc())
    noticias.extend(obter_noticias_da_ciencia())
    noticias.extend(obter_noticias_da_cnn())
    noticias.extend(obter_noticias_da_entretenimento())
    noticias.extend(obter_noticias_da_esportes())
    noticias.extend(obter_noticias_da_saude())
    noticias.extend(obter_noticias_da_tecnologia())
    noticias.extend(obter_noticias_da_wsj())

    # Remover duplicatas
    noticias_sem_duplicatas = []
    for n in noticias:
        if n not in noticias_sem_duplicatas:
            noticias_sem_duplicatas.append(n)

    resultados = []
    for n in noticias_sem_duplicatas:
        title = n.get("title")
        if title and (query is None or query in title):
            resultados.append(n)

    for resultado in resultados:
        data_publicacao = resultado["publishedAt"]
        resultado["publishedAt"] = parser.isoparse(data_publicacao)

    ordenar = request.GET.get("ordenar")
    if ordenar == "desc":
        resultados = sorted(resultados, key=lambda n: n["publishedAt"], reverse=True)
    elif ordenar == "asc":
        resultados = sorted(resultados, key=lambda n: n["publishedAt"])

    return render(
        request,
        "noticias/resultados_pesquisa.html",
        {"resultados": resultados, "query": query, "ordenar": ordenar},
    )


@login_required
def pagina_de_login(request):
    return redirect("noticias_principais")


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("noticias_principais"))

def login_view(request):
    form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("noticias_principais"))
        else:
            print(form.errors)

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'registration/login.html'


def detalhes_noticia(request, url_noticia):
    noticias = obter_noticias_principais()

    noticia_principal = None
    for n in noticias:
        if n.get("url") == url_noticia:
            noticia_principal = n
            break

    if noticia_principal == None:
        noticias = obter_noticias_da_bbc()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    if noticia_principal == None:
        noticias = obter_noticias_da_cnn()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    if noticia_principal == None:
        noticias = obter_noticias_da_wsj()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break
    
    if noticia_principal == None:
        noticias = obter_noticias_da_ciencia()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break
    
    if noticia_principal == None:
        noticias = obter_noticias_da_entretenimento()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    if noticia_principal == None:
        noticias = obter_noticias_da_esportes()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    if noticia_principal == None:
        noticias = obter_noticias_da_saude()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    if noticia_principal == None:
        noticias = obter_noticias_da_tecnologia()

        noticia_principal = None
        for n in noticias:
            if n.get("url") == url_noticia:
                noticia_principal = n
                break

    noticias_relacionadas = []
    for n in noticias:
        if (
            n.get("source.name") == noticia_principal.get("source.name")
            and n.get("url") != url_noticia
        ):
            noticias_relacionadas.append(n)

    noticias_relacionadas = noticias_relacionadas[:3]

    comentarios = Comentario.objects.filter(url_noticia=url_noticia)

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            texto = form.cleaned_data["texto"]

            if request.user.is_authenticated:
                Comentario.objects.create(
                    texto=texto, url_noticia=url_noticia, autor=request.user
                )
            else:
                Comentario.objects.create(
                    texto=texto, url_noticia=url_noticia, anonimo=True
                )

            return HttpResponseRedirect(request.path_info)

    return render(
        request,
        "noticias/detalhes_noticia.html",
        {
            "noticia_principal": noticia_principal,
            "noticias_relacionadas": noticias_relacionadas,
            "comentarios": comentarios,
            "form": ComentarioForm(),
        },
    )


def obter_noticias_da_bbc():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "sources": "bbc-news",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []


def obter_noticias_da_cnn():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "sources": "cnn",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []
    
def obter_noticias_da_wsj():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "sources": "the-wall-street-journal",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []


def obter_noticias_principais(categorias=[]):
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []


def noticias_principais(request):
    categorias = request.GET.getlist("categoria")
    noticias_principais = obter_noticias_principais(categorias)

    return render(
        request,
        "noticias/noticias_principais.html",
        {"noticias_principais": noticias_principais, "categorias": categorias},
    )


# Jornais
def noticias_bbc(request):
    bbc_noticias = obter_noticias_da_bbc()
    return render(request, "noticias/noticias_bbc.html", {"bbc_noticias": bbc_noticias})

def noticias_cnn(request):
    cnn_noticias = obter_noticias_da_cnn()
    return render(request, "noticias/noticias_cnn.html", {"cnn_noticias": cnn_noticias})

def noticias_wsj(request):
    wsj_noticias = obter_noticias_da_wsj()
    return render(request, "noticias/noticias_wsj.html", {"wsj_noticias": wsj_noticias})

# Categorias

def obter_noticias_da_ciencia():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": "science",
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []

def noticias_ciencia(request):
    ciencia_noticias = obter_noticias_da_ciencia()
    return render(request, "noticias/noticias_ciencia.html", {"ciencia_noticias":
        ciencia_noticias})

def obter_noticias_da_esportes():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": "sports",
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []

def noticias_esportes(request):
    esporte_noticias = obter_noticias_da_esportes()
    return render(request, "noticias/noticias_esportes.html", {"esporte_noticias":
        esporte_noticias})
    
def obter_noticias_da_entretenimento():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": "entertainment",
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []

def noticias_entretenimento(request):
    entretenimento_noticias = obter_noticias_da_entretenimento()
    return render(request, "noticias/noticias_entretenimento.html", {"entretenimento_noticias":
        entretenimento_noticias})
    
def obter_noticias_da_saude():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": "health",
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []

def noticias_saude(request):
    saude_noticias = obter_noticias_da_saude()
    return render(request, "noticias/noticias_saude.html", {"saude_noticias":
        saude_noticias})

def obter_noticias_da_tecnologia():
    api_key = API_KEY
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": "technology",
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        noticias = [noticia for noticia in noticias if noticia['title'] != '[Removed]' and isinstance(noticia.get('author', ''), str) and len(noticia['author']) <= 20]
        noticias = [noticia for noticia in noticias if noticia["urlToImage"]]
        
        for resultado in noticias:
            data_publicacao = resultado["publishedAt"]
            resultado["publishedAt"] = parser.isoparse(data_publicacao)
        
        return noticias
    else:
        return []

def noticias_tecnologia(request):
    tecnologia_noticias = obter_noticias_da_tecnologia()
    return render(request, "noticias/noticias_tecnologia.html", {"tecnologia_noticias":
        tecnologia_noticias})