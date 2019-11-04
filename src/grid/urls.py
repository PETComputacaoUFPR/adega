from django.conf.urls import url
from grid import views

urlpatterns = [
    url(r'^$', views.GridList.as_view(), name='GridList'),
    url(r'^detail/(?P<pk>\w+)/$', views.GridDetail.as_view(), name='GridDetailView'),
    url(r'^create/$', views.GridCreate.as_view(), name='GridCreateView'),
    # url(r'^update/(?P<pk>[0-9]+)/$', views.GridUpdate.as_view(), name='GridUpdateView'),
    url(r'^delete/(?P<pk>[0-9]+)$', views.GridDelete.as_view(), name='GridDeleteView'),
    ]
