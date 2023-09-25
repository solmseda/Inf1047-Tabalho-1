from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    #autor = models.ForeignKey(User, on_delete = models.CASCADE, related_name='blog_posts')
    corpo = models.TextField()
    dt_publicado = models.DateTimeField(default=timezone.now)
    dt_criado = models.DateTimeField(auto_now_add=True)
    dt_atualizado = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-dt_publicado']
        indexes = [models.Index(fields=['-dt_publicado'])]

    def __str__(self):
        return self.titulo