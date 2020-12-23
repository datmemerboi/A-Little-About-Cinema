from django.urls import path

from . import views

urlpatterns = [
	path('new/', views.NewDocHandler.as_view()),
	path('all/', views.MovieViewHandler.as_view()),
	path('retrieve/', views.RetrieveDocHandler.as_view()),
	path('update/', views.UpdateHandler.as_view()),
	path('delete/', views.DeleteHandler.as_view()),
	path('truncate/', views.TruncateHandler.as_view()),
	# re_path(r'alt/(?P<ID>(\w*|\w*\s)+\s\(\d{4}\))/', views.AltMovieViewHandler.as_view())
]