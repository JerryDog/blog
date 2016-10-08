from django.conf.urls import patterns, include, url
from online import views
from django.contrib import admin
admin.autodiscover()

 
urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^index/$',views.index,name = 'index'),
    url(r'^logout/$',views.logout,name = 'logout'),
    url(r'^blog/$',views.blog,name = 'blog'),
    url(r'^singleblog/(\d*)/$',views.singleblog,name = 'singleblog'),
    url(r'^comments/$',views.comments,name = 'comments'),
    url(r'^photo/$',views.photo,name = 'photo'),
    url(r'^linux/$',views.linux,name = 'linux'),
    url(r'^linux/(\d*)/$',views.singlelinux,name = 'singlelinux'),
    url(r'^django/$',views.django,name = 'django'),
    url(r'^django/(\d*)/$',views.singledjango,name = 'singledjango'),
    url(r'^python/$',views.python,name = 'python'),
    url(r'^python/(\d*)/$',views.singlepython,name = 'singlepython'),
    url(r'^aws/$',views.aws,name = 'aws'),
    url(r'^aws/(\d*)/$',views.singleaws,name = 'singleaws'),
    url(r'^others/$',views.others,name = 'others'),
    url(r'^others/(\d*)/$',views.singleothers,name = 'singleothers'),
    #url(r'^blog/$',views.blog,name = 'blog'),
)
