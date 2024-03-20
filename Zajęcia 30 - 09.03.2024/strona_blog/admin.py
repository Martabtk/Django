from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'create', 'publish', 'author']
    search_fields = ['title', 'body']
    #linijka która tworzy slug automatycznie na podstawie title
    prepopulated_fields = {'slug': ('title',)}
    #autor wyszukiwany po kluczu głównym w swojej tabeli
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
