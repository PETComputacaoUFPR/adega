from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from uploads import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^simple/$', views.simple_upload, name='simple'),
    url(r'^form/$', views.model_form_upload, name='model_form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
