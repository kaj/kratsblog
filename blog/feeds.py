# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from django.conf import settings
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from blog.models import Post

class AtomFeed(Feed):
    feed_type = Atom1Feed
    title = settings.SITE.get('sitename')
    link = "/"
    description = u"Nya %s" % title
    description_template = 'feeds/atom_description.html'

    def items(self):
        return Post.objects.exclude(posted_time__exact=None)[:7]

    def item_pubdate(self, item):
        return item.posted_time
    def item_updateddate(self, item):
        return item.updated_at

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
