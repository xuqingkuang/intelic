# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth.urls import patterns, url

import views, apis

urlpatterns = patterns('',
    url(r'^build-list/$', views.BuildListView.as_view(), name='build_list'),
    url(r'^new-build/$', views.BuildCreateView.as_view(), name='build_create'),
    url(r'^new-build/$', views.BuildCreateView.as_view(), name='build_create'),
    url(r'^build/(?P<slug>[-\w]+)/$', views.BuildDetailView.as_view(), name='build_detail'),
    url(r'^build/(?P<slug>[-\w]+).txt$', views.BuildConfigDownloadView.as_view(), name='build_download_config_file'),

    url(r'apis/get-baselines/', apis.get_baselines, name='builder_api_get_baselines'),
    url(r'apis/get-components-form/', apis.get_components_form, name='builder_api_get_components_form'),
)
