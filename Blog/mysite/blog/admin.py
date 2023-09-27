from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', 'autor', 'dt_publicado', 'status']
    list_filter = ['status', 'dt_criado', 'dt_publicado', 'autor']
    search_fields = ['autor']
    prepopulated_fields = {'slug': ('titulo',)}
    raw_id_fields = ['autor']
    date_hierarchy = 'dt_publicado'
    ordering = ['status', 'dt_publicado']