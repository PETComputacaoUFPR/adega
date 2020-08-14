
from django.conf.urls import include, url
from django.contrib import admin

from adega import views

from django.views.generic import RedirectView

urlpatterns = [
    #url(r'^$', RedirectView.as_view(url='/')),

    url(r'^$', views.dashboard, name='dashboard'),

    url(r'^admission/(?P<submission_id>\w*)/', include('admission.urls', namespace='admission')),

    url(r'^course/(?P<submission_id>\w*)/', include('course.urls', namespace='course')),

    url(r'^submission/', include('submission.urls', namespace='submission')),

    url(r'^grid/(?P<degree_code>\w+)/', include('grid.urls', namespace='grid')),

    url(r'^student/(?P<submission_id>\w*)/', include('student.urls', namespace='student')),

    url(r'^degree/(?P<submission_id>\w*)/', include('degree.urls', namespace='degree')),

    url(r'^cepe9615/(?P<submission_id>\w*)/', include('cepe9615.urls', namespace='cepe9615')),

    url(r'^public/', include('public.urls', namespace='public')),

    url(r'^logout/$', views.logout, name='logout'),

    url(r'^admin/', admin.site.urls),
]
