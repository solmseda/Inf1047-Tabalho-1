from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_lista, name='lista_postagens'),
    path('<int:id>/', views.detalhes_postagem, name='detalhes_postagem'),
    path('novaPostagem/criar_postagem', views.criar_postagem, name='criar_postagem'),
    path('editar_postagem/<int:id>/', views.editar_postagem, name='editar_postagem'),
    path('confirmar_exclusao/<int:id>/', views.confirmar_exclusao, name='confirmar_exclusao'),
    path('deletar_postagem/<int:id>/', views.deletar_postagem, name='deletar_postagem'),
]