from django.db import models

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_publicacao = models.DateTimeField()

class Comentario(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
