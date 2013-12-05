from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse
from django.conf.urls.static import static
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

class HomeRedirectView(RedirectView):
    permanent = False
    def get_redirect_url(self):
        # it would be better to use reverse here
        return reverse('build_list')

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomeRedirectView.as_view(), name='home'),
    # url(r'^intelic/', include('intelic.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^builder/', include('intelic.builder.urls')),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('intelic.account.urls')),
)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
