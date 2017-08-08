from django.conf.urls import url
from course import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^compare', views.compare, name='compare'),
    url(r'^(?P<course_code>\w+)/$', views.detail, name='detail'),
]
