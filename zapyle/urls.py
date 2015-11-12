from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^track/$', 'coreapp.views.tweets', name='tweets'),
    url(r'^most_used/$', 'coreapp.views.most_used', name='most_used'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
