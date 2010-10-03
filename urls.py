from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from blog import views as blog

urlpatterns = patterns(
    '',
    # Example:
    # (r'^kratsblog/', include('kratsblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url('^$', blog.index),
    url('^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[a-z-]+)',
        blog.post_detail)
)

if settings.DEBUG and settings.MEDIA_URL[0] == '/':
    urlpatterns += patterns(
        '',
        #url('500', direct_to_template, {'template': '500.html'}),
        #url('404', direct_to_template, {'template': '404.html'}),
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
