# -*- encoding: utf-8 -*-
"""
Test creating content through the admin interface.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from blog.models import Post
from datetime import datetime
from lxml import html
import re

class SimpleTest(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_superuser(
            username = 'admin',
            email = 'admin@blog.tld',
            password = 'foo17bar',
            first_name = 'Adam',
            last_name = 'Minutis',
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
        return html_from_resp(response)
        
    def test_admin_home(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='foo17bar'))
        doc = self.get('/admin/')
        self.assertEqual(['Django-administration', 'Webbplatsadministration'],
                         find_text(doc, 'h1'))
        self.assertEqual([('Lägg till', '/admin/blog/post/add/')],
                         [(a.text_content(), a.get('href'))
                           for a in doc.cssselect('.app-blog .model-post .addlink')])

    def xtest_add_unpublished_post(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='foo17bar'))
        doc = self.get('/admin/blog/post/add/')
        self.assertEqual(['Django-administration', 'Lägg till post'],
                         find_text(doc, 'h1'))
        form = HtmlForm(self.client, doc.cssselect('form'))
        form.referer = '/admin/blog/post/add/'
        form['title'] = 'Exempel'
        form['content'] = 'Ett litet exempel.\n\nI två stycken.'
        form.submit()

    def test_add_published_posts(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='foo17bar'))
        doc = self.get('/admin/blog/post/add/')
        self.assertEqual(['Django-administration', 'Lägg till post'],
                         find_text(doc, 'h1'))
        form = HtmlForm(self.client, doc.cssselect('form'))
        form.referer = '/admin/blog/post/add/'
        form['title'] = 'Exempel'
        form['content'] = 'Ett litet exempel.\n\nI två stycken.'
        form['posted_time_0'] = '2018-01-01'
        form['posted_time_1'] = '22:47:32'
        resp = form.submit()
        self.assertEqual(302, resp.status_code)
        m = re.match('/admin/blog/post/([0-9]+)/change/', resp.get('Location'))
        self.assertTrue(m, 'Unexected redirect, got %r' % resp.get('Location'))
        post = Post.objects.get(id=m.group(1))
        self.assertEqual(('Exempel', '/2018/01/exempel'),
                         (post.title, post.get_absolute_url()))

        doc = self.get('/admin/blog/post/add/')
        form = HtmlForm(self.client, doc.cssselect('form'))
        form.referer = '/admin/blog/post/add/'
        form['title'] = 'Exempel'
        form['content'] = 'Samma titel annan månad, inte kollision.'
        form['posted_time_0'] = '2018-02-17'
        form['posted_time_1'] = '13:37:00'
        resp = form.submit()
        self.assertEqual(302, resp.status_code)
        m = re.match('/admin/blog/post/([0-9]+)/change/', resp.get('Location'))
        self.assertTrue(m, 'Unexected redirect, got %r' % resp.get('Location'))
        post = Post.objects.get(id=m.group(1))
        self.assertEqual(('Exempel', '/2018/02/exempel'),
                         (post.title, post.get_absolute_url()))

        doc = self.get('/admin/blog/post/add/')
        form = HtmlForm(self.client, doc.cssselect('form'))
        form.referer = '/admin/blog/post/add/'
        form['title'] = 'Exempel'
        form['content'] = 'Samma titel samma månad.  Kollision att hantera.'
        form['posted_time_0'] = '2018-02-23'
        form['posted_time_1'] = '13:37:00'
        resp = form.submit()
        self.assertEqual(302, resp.status_code)
        m = re.match('/admin/blog/post/([0-9]+)/change/', resp.get('Location'))
        self.assertTrue(m, 'Unexected redirect, got %r' % resp.get('Location'))
        post = Post.objects.get(id=m.group(1))
        self.assertEqual(('Exempel', '/2018/02/exempel-2'),
                         (post.title, post.get_absolute_url()))

def find_text(doc, selector):
    return [e.text_content() for e in doc.cssselect(selector)]

class HtmlForm():
    def __init__(self, driver, form_soup):
        self.driver = driver
        assert form_soup, "No such form"
        if isinstance(form_soup, list) and len(form_soup) == 1:
            self.form_soup = form_soup[0]
        else:
            self.form_soup = form_soup
        self.values = {}
        self.legal_values = {}
        self.select_values = {}
        #self.referer = driver.last_visited_url

        for elem in self.form_soup.cssselect('input[name]'):
            name = elem.get('name')
            if elem.get('type') in ['checkbox', 'radio']:
                # Note: this is not complete or sane!
                value = elem.get('value', True)
                self.legal_values.setdefault(name, set( [True, False] if value in [True, False] else [] )
                                            ).add(value)
                if elem.get('checked') or elem.get('selected'):
                    self.values[name] = value
                elif not name in self.values:
                    self.values[name] = None
            else:
                self.values[name] = elem.get('value')

        for elem in self.form_soup.cssselect('textarea'):
            name = elem.get('name')
            self.values[name] = elem.text_content().replace('&quot;', '"') \
                .replace('&lt;', '<').replace('&gt;', '>') \
                .replace('&amp;', '&')

        for elem in self.form_soup.cssselect('select'):
            name = elem['name']
            self.values[name] = None # Make it exist if no default value
            self.legal_values[name] = set()
            self.select_values[name] = {}
            for option in select(elem, 'option'):
                value = option['value']
                self.legal_values[name].add(value)
                self.select_values[name][option.getText().strip()] = value
                if option.has_attr('selected'):
                    self.values[name] = value
            print("Select %s: %s" % (name, self.values.get(name)))

        for elem in self.form_soup.cssselect('button'):
            if elem.get('name', None):
                name = elem['name']
                value = elem.get('value', True) # NOTE: MSIE uses content instead!
                self.legal_values.setdefault(name, set()).add(value)
                self.values.setdefault(name, None)

    def labels(self, labelid):
        return [l.getText() for l in self.form_soup.findAll('label', {'for':re.compile("^%s"%labelid)})]

    def __setitem__(self, key, value):
        assert key in self.values, u'Form has no %s, valid fields are: %s' % (key, self.values.keys())
        if key in self.select_values:
            # Currently support both "user" and "code" values.
            # TODO: Fix the tests to allways use user values and support only that.
            if value in self.select_values[key]:
                value = self.select_values[key][value]

        if key in self.legal_values:
            if isinstance(value, set):
                for v in value:
                    assert v in self.legal_values[key], u'%s is not a legal value for %s in form, valid values are: %s' % (value, key, self.legal_values[key])
            else:
                assert value in self.legal_values[key], u'%s is not a legal value for %s in form, valid values are: %s' % (value, key, self.select_values.get(key) or self.legal_values[key])
        self.values[key] = value

    def __getitem__(self, key):
        assert key in self.values, u'Form has no %s, valid fields are: %s' % (key, self.values.keys())
        return self.values[key]

    def submit(self, base_url=None, **kwargs):
        method = self.form_soup.get('method', 'get').lower()
        action = self.form_soup.get('action')
        if action == '.' or action == '':
            action = base_url or self.referer
        enctype = self.form_soup.get('enctype', 'application/x-www-form-urlencoded')

        self.values = {k: v for k, v in self.values.items() if k and v}

        #print(u"Submitting to %s using %s method: %s" % (action, method, self.values))
        # NOTE Ignoring enctype attribute

        if method == 'get':
            data = urlencode(self.values)
            return self.driver.get(action + '?' + data)

        if method == 'post':
            if 'HTTP_REFERER' not in kwargs:
                kwargs['HTTP_REFERER'] = self.referer
            #print("kwargs is", kwargs)
            return self.driver.post(action, self.values, **kwargs)

    def unset(self, name):
        del self.values[name]

def html_from_resp(response):
    body = response.content
    if body:
        return html.document_fromstring(body.decode(response.charset))
    else:
        return None
