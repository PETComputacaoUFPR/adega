from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^uploads/', include('uploads.urls', namespace='uploads')),

    url(r'^admin/', admin.site.urls),
]
