from django.contrib import admin
from django.urls import path, include, re_path
import movies.urls
import categories.urls
from .views import IndexHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexHandler),
    path('movie/', include(movies.urls)),
    path('category/', include(categories.urls))
]
