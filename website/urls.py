from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    # Examples:
    url(r'^sitemap\.xml$', 'website.views.sitemap', name='sitemap'),
    url(r'^$', 'website.views.home', name='home'),
    url(r'^(?P<city>[a-z-]+)$', 'website.views.city', name='city'),
    url(r'^(?P<city>[a-z-]+)/ecosystem$', 'website.views.city_ecosystem', name='city_ecosystem'),
    # url(r'^blog/', include('blog.urls')),

)
