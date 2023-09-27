from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_lista, name='post_lista'),
    path('<int:id>/', views.post_detalhes, name='post_detalhes'),
    path('novaPostagem/criar_postagem', views.criar_postagem, name='criar_postagem'),
]