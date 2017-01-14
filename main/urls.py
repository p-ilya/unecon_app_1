from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rasp/$', views.rasp, name='criteria'),
    url(r'^info/$', views.info, name='info'),
    url(r'^rasp/show/$', views.show_rasp, name='show_rasp'),
]
   
