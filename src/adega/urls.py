
from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^submission/', include('uploads.urls', namespace='uploads')),

    url(r'^admission/(?P<submission_id>\w*)/', include('admission.urls', namespace='admission')),
    
    url(r'^course/(?P<submission_id>\w*)/', include('course.urls', namespace='course')),
    
    url(r'^student/(?P<submission_id>\w*)/', include('student.urls', namespace='student')),
    
    url(r'^degree/(?P<submission_id>\w*)/', include('degree.urls', namespace='degree')),

    url(r'^public/', include('public.urls', namespace='public')),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),
]
