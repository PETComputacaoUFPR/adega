from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^uploads/', include('uploads.urls', namespace='uploads')),

    url(r'^public/', include('public.urls', namespace='public')),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),
]
