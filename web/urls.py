from django.urls import path
from . import views

app_name = 'web'
urlpatterns = [
	path('', views.index, name='index'),
	path('video/', views.video, name='video')
]