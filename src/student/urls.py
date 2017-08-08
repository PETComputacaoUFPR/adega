from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<grr>GRR\d{8})/$', views.detail, name='detail'),
]
