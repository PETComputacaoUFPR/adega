from django.conf.urls import url
from degree import views
urlpatterns = [url(r'^$',views.index, name='index')
        ]
