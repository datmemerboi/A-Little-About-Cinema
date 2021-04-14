from django.urls import path

from . import views

urlpatterns = [
	path('new/', views.CreateHandler.as_view()),
	path('all/', views.ViewHandler.as_view()),
	path('retrieve/', views.RetrieveHandler.as_view()),
	path('update/', views.UpdateHandler.as_view()),
	path('delete/', views.DeleteHandler.as_view()),
	path('truncate/', views.TruncateHandler.as_view())
]