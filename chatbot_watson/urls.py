from django.conf.urls import url

from . import views

urlpatterns = [
 #   url(r'^$', views.index, name='index'),
 	url(r'^63f293181b76424e5668ed7cd3dd7a12692c0a566806c654a1/?$', views.bot.as_view()),
       
]