from django.urls import path
from .router import router
from .views import NewDocHandler

urlpatterns = [
	path('new/', NewDocHandler)
]

urlpatterns += router.urls