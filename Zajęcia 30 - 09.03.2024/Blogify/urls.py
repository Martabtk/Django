from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('strona_blog/', include('strona_blog.urls', namespace='strona_blog')),
]