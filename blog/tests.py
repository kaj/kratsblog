"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    
    def setUp(self):
        self.c = Client()
    
    def get(self, url, expected_status_code=200, expected_location=''):
        response = self.c.get(url)
        self.assertEqual((expected_status_code, expected_location, 
                          'text/html; charset=utf-8'),
                         (response.status_code,
                          response.get('Location', '') \
                              .replace('http://testserver', ''),
                          response['Content-Type']))

        # TODO Parse the document tree and do some useful stuff
        #parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"),
        #                             strict=True, namespaceHTMLElements=False)
        
        try:
            return response.content
            #if response.content:
            #    return parser.parse(response.content)
            #else:
            #    return None

        except Exception:
            # NOTE Even though parser.errors is an array, it contains only first error.
            self.fail("Response is NOT valid HTML5: %s" %
                      ["%s, element: %s, pos: %s" % (error, element.get('name'), pos)
                       for pos, error, element in parser.errors])
        
    def test_get_frontpage(self):
        doc = self.get('/')
