
from django.conf.urls import include, url
from django.contrib import admin

from . import views

from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/adega/')),

    url(r'^adega/$', views.dashboard, name='dashboard'),

    url(r'^adega/admission/(?P<submission_id>\w*)/', include('admission.urls', namespace='admission')),

    url(r'^adega/course/(?P<submission_id>\w*)/', include('course.urls', namespace='course')),

    url(r'^adega/submission/', include('submission.urls', namespace='submission')),

    url(r'^adega/student/(?P<submission_id>\w*)/', include('student.urls', namespace='student')),

    url(r'^adega/degree/(?P<submission_id>\w*)/', include('degree.urls', namespace='degree')),

    url(r'^adega/public/', include('public.urls', namespace='public')),

    url(r'^adega/logout/$', views.logout, name='logout'),

    url(r'^adega/admin/', admin.site.urls),
]
