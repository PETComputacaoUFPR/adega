from django.conf.urls import include, url
from faq import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.question_list, name='question_list'),
   
    url(r'^/question_new', views.question_new, name='question_new'),

]

