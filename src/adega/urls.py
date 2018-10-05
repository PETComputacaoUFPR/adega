
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^adega/$', views.dashboard, name='dashboard'),

    url(r'^adega/uploads/', include('uploads.urls', namespace='uploads')),

    url(r'^adega/admission/(?P<degree_id>\w*)/', include('admission.urls', namespace='admission')),
    
    url(r'^adega/course/(?P<degree_id>\w*)/', include('course.urls', namespace='course')),
    
    url(r'^adega/degree/(?P<degree_id>\w*)/', include('degree.urls', namespace='degree')),

    url(r'^adega/public/', include('public.urls', namespace='public')),

    url(r'^adega/logout/$', views.logout, name='logout'),

    url(r'^adega/admin/', admin.site.urls),
]
