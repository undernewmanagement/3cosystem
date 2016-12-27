from django.conf.urls import patterns, include, url
from django.contrib import admin

from website import views as ws

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sitemap\.xml$', ws.sitemap, name='sitemap'),
    url(r'^$', ws.home, name='home'),
    url(r'^(?P<city>[a-z-]+)$', ws.city, name='city'),
]
