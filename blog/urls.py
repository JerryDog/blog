from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(django.contrib.admin.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^online/', include('online.urls',namespace='online')),
    url(r'^$', include('online.urls',namespace='online')),
)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
