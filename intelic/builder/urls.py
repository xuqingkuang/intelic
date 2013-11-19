# The views used below are normally mapped in django.contrib.admin.urls.py
# This URLs file is used to provide a reliable view deployment for test purposes.
# It is also provided as a convenience to those who want to deploy these URLs
# elsewhere.

from django.contrib.auth.urls import patterns, url

import views, apis

urlpatterns = patterns('',
    url(r'^job-list/$', views.JobListView.as_view(), name='job_list'),
    url(r'^new-job/$', views.JobCreateView.as_view(), name='job_create'),
    
    url(r'apis/get-products/', apis.get_products, name='builder_api_get_product'),
    url(r'apis/get-components-form/', apis.get_components_form, name='builder_api_get_components_form'),
)
