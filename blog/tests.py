# -*- encoding: utf-8 -*-
"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from blog.models import Post
from datetime import datetime
from lxml import html

class SimpleTest(TestCase):
    
    def setUp(self):
        Post.objects.create(
            title='Hello World',
            content='Hello there, this is a test article\n\n' +
            'Containing two paragraphs of text.',
            posted_time=datetime(2017, 12, 17, 23, 45, 0)
        )
    
    def get(self, url, expected_status_code=200, expected_location='',
            expected_contenttype='text/html; charset=utf-8'):
        response = self.client.get(url)
        self.assertEqual((expected_status_code, expected_location, 
                          expected_contenttype),
                         (response.status_code,
                          response.get('Location', '') \
                              .replace('http://testserver', ''),
                          response['Content-Type']))

        if response.content:
            return html.document_fromstring(response.content)
        else:
            return None
        
    def test_get_frontpage(self):
        doc = self.get('/')
        self.assertEquals(['Tygbittar.krats.se'], find_text(doc, 'h1'))
        self.assertEquals(['Hello World'], find_text(doc, '#main h2'))
        link, = doc.cssselect('#main h2 a')
        self.assertEquals('/2017/12/hello-world', link.get('href'))

    def test_get_article(self):
        doc = self.get('/2017/12/hello-world')
        self.assertEquals(['Hello World'], find_text(doc, '#main h2'))
        self.assertEquals(['17 december 2017 23:45'], find_text(doc, '#main p.dateline'))
        self.assertEquals(['Hello there, this is a test article',
                           'Containing two paragraphs of text.'],
                          find_text(doc, '#main .postContent p'))

    def test_get_feed(self):
        feed = self.get('/atom.xml',
                        expected_contenttype='application/atom+xml; charset=utf-8')

def find_text(doc, selector):
    return [e.text_content() for e in doc.cssselect(selector)]
