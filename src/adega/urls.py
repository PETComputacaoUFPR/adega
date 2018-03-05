from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^uploads/', include('uploads.urls', namespace='uploads')),

    url(r'^login/', views.login, name='login'),

    url(r'^admin/', admin.site.urls),
]
