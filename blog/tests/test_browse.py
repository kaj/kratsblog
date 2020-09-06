# -*- encoding: utf-8 -*-
"""
Create some simple content and test browsing the site.
"""

from django.test import TestCase
from blog.models import Post
from datetime import datetime
from lxml import html

class SimpleTest(TestCase):
    
    def setUp(self):
        # Create three posts with same title, two in same month, to see
        # the slug generation works as it should.
        Post.objects.create(
            title='Hello World',
            content='Hello there, this is a test article\n\n' +
            'Containing two paragraphs of text.',
            posted_time=datetime(2017, 11, 27, 14, 15, 0)
        )
        Post.objects.create(
            title='Hello World',
            content='Hello there, this is a test article\n\n' +
            'Containing two paragraphs of text.',
            posted_time=datetime(2017, 12, 17, 23, 45, 0)
        )
        Post.objects.create(
            title='Hello World',
            content='Hello there, this is a second test article\n\n' +
            'It is newer, so it will be displayed first..',
            posted_time=datetime(2017, 12, 18, 7, 30, 0)
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
        self.assertEqual(['Tygbittar.krats.se'], find_text(doc, 'h1'))
        self.assertEqual(['Hello World', 'Hello World', 'Hello World'],
                         find_text(doc, '#main h2'))
        self.assertEqual(['/2017/12/hello-world-2',
                          '/2017/12/hello-world',
                          '/2017/11/hello-world'],
                         [l.get('href') for l in doc.cssselect('#main h2 a')])

    def test_get_article(self):
        doc = self.get('/2017/12/hello-world')
        self.assertEqual(['Hello World'], find_text(doc, '#main h2'))
        publine, = find_text(doc, '#main p.dateline')
        self.assertTrue('17 december 2017 23:45' in publine, publine)
        self.assertEqual(['Hello there, this is a test article',
                          'Containing two paragraphs of text.'],
                         find_text(doc, '#main .postContent p'))

    def test_get_feed(self):
        feed = self.get('/atom.xml',
                        expected_contenttype='application/atom+xml; charset=utf-8')

def find_text(doc, selector):
    return [e.text_content() for e in doc.cssselect(selector)]
