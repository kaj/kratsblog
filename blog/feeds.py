# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from blog.models import Post
from django.contrib.sites.models import Site

class AtomFeed(Feed):
    feed_type = Atom1Feed
    current_site = Site.objects.get_current()
    title = current_site.name
    link = "/"
    description = u"Nya %s" % current_site.name
    description_template = 'feeds/atom_description.html'

    def items(self):
        return Post.objects.exclude(posted_time__exact=None)[:7]

    def item_pubdate(self, obj):
        return obj.posted_time

    def item_author_name(self, item):
        return u'Katarina Kaj'

    def item_author_email(self, item):
        return 'katy@kth.se'

    def item_title(self, item):
        return item.title
    
    #def item_categories(self, item):
    #    categories = []
    #    if item.album:
    #        if item.album.suite:
    #            categories.append(item.album.suite)
    #        categories.append(item.album)
    #    return categories

class RssFeed(AtomFeed):
    feed_type = Rss201rev2Feed
    description_template = 'feeds/rss_description.html'
