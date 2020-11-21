from django.contrib import admin
from django.urls import path, include, re_path
import movies.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie/', include(movies.urls))
]
