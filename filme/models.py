from typing import Tuple

from django.db import models
from django.db.transaction import mark_for_rollback_on_error
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

LISTA_CATEGORIAS: tuple[tuple[str, str], tuple[str, str], tuple[str, str], tuple[str, str]] = (
    ("CRYPTO","Crypto"),
    ("RENDA FIXA ","Renda Fixa"),
    ("RENDA VARIAVEL","Renda Variável"),
    ("FIIS","Fiis"),
)

class Filme(models.Model):
    titulo = models.CharField(max_length=100)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

class Episodeo(models.Model):
    filme = models.ForeignKey("Filme",related_name="episodeos", on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + ' - ' +self.titulo

class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")