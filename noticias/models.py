from django.db import models
from django import forms
from django.contrib.auth.models import User


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField()

class Comentario(models.Model):
    texto = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)
    url_noticia = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    anonimo = models.BooleanField(default=False)
