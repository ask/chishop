import unittest
import StringIO
from djangopypi.views import parse_distutils_request
from djangopypi.models import Project, Classifier
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

def create_post_data(action):
    data = {
            ":action": action,
            "metadata_version": "1.0",
            "name": "foo",
            "version": "0.1.0-pre2",
            "summary": "The quick brown fox jumps over the lazy dog.",
            "home_page": "http://example.com",
            "author": "Foo Bar Baz",
            "author_email": "foobarbaz@example.com",
            "license": "Apache",
            "keywords": "foo bar baz",
            "platform": "UNKNOWN",
            "classifiers": [
                "Development Status :: 3 - Alpha",
                "Environment :: Web Environment",
                "Framework :: Django",
                "Operating System :: OS Independent",
                "Intended Audience :: Developers",
                "Intended Audience :: System Administrators",
                "License :: OSI Approved :: BSD License",
                "Topic :: System :: Software Distribution",
                "Programming Language :: Python",
            ],
            "download_url": "",
            "provides": "",
            "requires": "",
            "obsoletes": "",
            "description": """
=========
FOOBARBAZ
=========

Introduction
------------
    ``foo`` :class:`bar`
    *baz*
    [foaoa]
            """,
    }
    return data

def create_request(data):
    boundary = '--------------GHSKFJDLGDS7543FJKLFHRE75642756743254'
    sep_boundary = '\n--' + boundary
    end_boundary = sep_boundary + '--'
    body = StringIO.StringIO()
    for key, value in data.items():
        # handle multiple entries for the same name
        if type(value) not in (type([]), type( () )):
            value = [value]
        for value in value:
            value = unicode(value).encode("utf-8")
            body.write(sep_boundary)
            body.write('\nContent-Disposition: form-data; name="%s"'%key)
            body.write("\n\n")
            body.write(value)
            if value and value[-1] == '\r':
                body.write('\n')  # write an extra newline (lurve Macs)
    body.write(end_boundary)
    body.write("\n")

    return body.getvalue()


class MockRequest(object):

    def __init__(self, raw_post_data):
        self.raw_post_data = raw_post_data
        self.META = {}


class TestParseWeirdPostData(unittest.TestCase):

    def test_weird_post_data(self):
        data = create_post_data("submit")
        raw_post_data = create_request(data)
        post, files = parse_distutils_request(MockRequest(raw_post_data))
        self.assertTrue(post)

        for key in post.keys():
            if isinstance(data[key], list):
                self.assertEquals(data[key], post.getlist(key))
            elif data[key] == "UNKNOWN":
                self.assertTrue(post[key] is None)
            else:
                self.assertEquals(post[key], data[key])

class TestSearch(unittest.TestCase):
    
    def setUp(self):
        data = create_post_data("submit")
        dummy_user = User.objects.create(username='krill', password='12345',
                                         email='krill@opera.com')
        Project.objects.create(name=data['name'], license=data['license'],
                               summary=data["summary"], owner=dummy_user)
        
        
    def testSearchForPackage(self):
        client = Client()
        response = client.post(reverse('djangopypi-search'), {'search_term': 'foo'})
        self.assertTrue("The quick brown fox jumps over the lazy dog." in response.content)
