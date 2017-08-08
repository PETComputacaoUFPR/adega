from django.conf.urls import url
from admission import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<year>\d{4})/(?P<semester>\w+)/$', views.detail, name='detail'),
]
