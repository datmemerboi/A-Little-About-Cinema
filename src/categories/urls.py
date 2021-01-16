from django.urls import path

from . import views

urlpatterns = [
	path('new/', views.NewCategoryHandler.as_view()),
	path('all/', views.CategoryViewHandler.as_view()),
	path('retrieve/', views.RetrieveHandler.as_view()),
	path('sync/', views.ResyncHandler.as_view()),
	path('clear/', views.ClearListHandler.as_view())
]