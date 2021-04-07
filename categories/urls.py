from django.urls import path

from . import views

urlpatterns = [
	path('new/', views.CreateHandler.as_view()),
	path('all/', views.ViewHandler.as_view()),
	path('retrieve/', views.RetrieveHandler.as_view()),
	path('sync/', views.ResyncHandler.as_view()),
	path('clear/', views.ClearListHandler.as_view()),
	path('edit/', views.UpdateHandler.as_view())
]