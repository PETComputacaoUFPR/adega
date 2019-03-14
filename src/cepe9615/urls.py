from django.conf.urls import url
from cepe9615 import views

urlpatterns = [
        url(r'^$', views.index, name='index')
]
