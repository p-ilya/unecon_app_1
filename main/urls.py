from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rasp/$', views.rasp, name='criteria'),
    url(r'^info/$', views.info, name='info'),
    url(r'^show/(?P<since>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<to>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<teacher>[0-9]+)/(?P<method>[0-9]{1})/$', 
    	views.show_rasp, 
    	name='show_rasp'),
    
    url(r'^teacher_autocomplete/$', 
    	views.TeacherAutocomplete.as_view(), 
    	name='teacher_autocomplete'),

    url(r'^send/text/(?P<mailto>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,4})/',
    	views.send_text_email,
    	name='send_text_email'),
 ]