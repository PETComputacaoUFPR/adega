from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^create/', views.SubmissionCreate.as_view(), name='SubmissionCreateView'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.SubmissionUpdate.as_view(), name='SubmissionUpdateView'),
    url(r'^delete/(?P<pk>[0-9]+)$', views.SubmissionDelete.as_view(), name='SubmissionDeleteView'),
    url(r'^', views.SubmissionList.as_view(), name='SubmissionListView'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.SubmissionDetail.as_view(), name='SubmissionDetailView'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
