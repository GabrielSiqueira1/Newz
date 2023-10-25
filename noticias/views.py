import requests
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Comentario
from .forms import ComentarioForm
from django.contrib.auth import login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from dateutil import parser


def resultados_pesquisa(request):
    query = request.GET.get("q")
    noticias = obter_noticias_principais()
    ordenar = request.GET.get("ordenar")

    resultados = []
    for n in noticias:
        if query in n.get("title"):
            resultados.append(n)

    for resultado in resultados:
        data_publicacao = resultado["publishedAt"]
        resultado["publishedAt"] = parser.isoparse(data_publicacao)

    if ordenar == "desc":
        resultados = sorted(resultados, key=lambda n: n["publishedAt"], reverse=True)
    elif ordenar == "asc":
        resultados = sorted(resultados, key=lambda n: n["publishedAt"])

    return render(
        request,
        "noticias/resultados_pesquisa.html",
        {"resultados": resultados, "query": query},
    )


@login_required
def pagina_de_login(request):
    return redirect("noticias_principais")


def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("noticias_principais"))


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("noticias_principais"))

    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


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
    api_key = "11f9a62b34e0465e867c2b4a400730d5"
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "sources": "bbc-news",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        return noticias
    else:
        return []


def obter_noticias_da_cnn():
    api_key = "11f9a62b34e0465e867c2b4a400730d5"
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": api_key,
        "sources": "cnn",
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
        return noticias
    else:
        return []


def obter_noticias_principais(categorias=[]):
    api_key = "11f9a62b34e0465e867c2b4a400730d5"
    url = "https://newsapi.org/v2/top-headlines?country=us"
    params = {
        "apiKey": api_key,
        "category": ",".join(categorias),
        "pageSize": 100,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        noticias = response.json().get("articles", [])
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


def noticias_bbc(request):
    bbc_noticias = obter_noticias_da_bbc()
    return render(request, "noticias/noticias_bbc.html", {"bbc_noticias": bbc_noticias})


def noticias_cnn(request):
    cnn_noticias = obter_noticias_da_cnn()
    return render(request, "noticias/noticias_cnn.html", {"cnn_noticias": cnn_noticias})
