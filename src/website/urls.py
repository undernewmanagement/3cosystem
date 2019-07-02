from django.conf.urls import include, url
from django.contrib import admin

from website import views as ws

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^sitemap\.xml$', ws.sitemap, name='sitemap'),
    url(r'^$', ws.home, name='home'),
    url(r'^(?P<city>[a-z-]+)$', ws.city, name='city'),
]
