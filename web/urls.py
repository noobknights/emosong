from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
	path('', views.index, name='index'),
	path('main', views.main, name='main'),
]