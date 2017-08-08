"""adega URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from adega import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^developers/', views.developers, name='developers'),
    url(r'^public/', include('public.urls', namespace='public')),
#    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': 'public:index'}, name='logout'),
    url(r'^(?P<degree_id>\w*)/', include('degree.urls', namespace='degree')),
    url(r'^(?P<degree_id>\w*)/students/', include('student.urls', namespace='student')),
    url(r'^(?P<degree_id>\w*)/admission/', include('admission.urls', namespace='admission')),
    url(r'^(?P<degree_id>\w*)/courses/', include('course.urls', namespace='course')),
#    url(r'^(?P<degree_id>\w*)/others/', include('other.urls', namespace='other')),
]
