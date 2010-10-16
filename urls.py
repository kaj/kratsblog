from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.generic.simple import direct_to_template
admin.autodiscover()

from blog import views as blog
from blog import feeds

feeds = { 'atom' : feeds.AtomFeed, 
          'rss'  : feeds.RssFeed, }

urlpatterns = patterns(
    '',
    # Example:
    # (r'^kratsblog/', include('kratsblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url('^$', blog.index),
    url('^(?P<year>[0-9]{4})/$', blog.index),
    url('^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', blog.index),
    url('^(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[a-z-]+)',
        blog.post_detail),
    url('^node/(?P<id>[0-9]+)', blog.redirect_from_id),
    (r'^(?P<url>(atom|rss)).xml$', 'django.contrib.syndication.views.feed',
     {'feed_dict': feeds}
     ),
    url('robots.txt', direct_to_template, 
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),
)

if settings.DEBUG and settings.MEDIA_URL[0] == '/':
    urlpatterns += patterns(
        '',
        url('500', direct_to_template, {'template': '500.html'}),
        url('404', direct_to_template, {'template': '404.html'}),
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
