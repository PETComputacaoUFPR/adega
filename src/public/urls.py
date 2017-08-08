from django.conf.urls import url
from django.contrib.auth.views import login
from public import views

urlpatterns = [
    url(r'^$', login, {'template_name':'public/index.html'}, name="index"),
]
