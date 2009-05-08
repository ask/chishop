"""
Management command for loading all the known classifiers from the official
pypi, or from a file/url.

Note, pypi docs says to not add classifiers that are not used in submitted
projects. On the other hand it can be usefull to have a list of classifiers
to choose if you have to modify package data. Use it if you need it.
"""

from __future__ import with_statement
import urllib
import os.path

from django.core.management.base import BaseCommand
from djangopypi.models import Classifier

CLASSIFIERS_URL = "http://pypi.python.org/pypi?%3Aaction=list_classifiers"

class Command(BaseCommand):
    help = """Load all classifiers from pypi. If any arguments are given,
they will be used as paths or urls for classifiers instead of using the
official pypi list url"""

    def handle(self, *args, **options):
        args = args or [CLASSIFIERS_URL]

        cnt = 0
        for location in args:
            print "Loading %s" % location
            lines = self._get_lines(location)
            for name in lines:
                c, created = Classifier.objects.get_or_create(name=name)
                if created:
                    c.save()
                    cnt += 1

        print "Added %s new classifiers from %s source(s)" % (cnt, len(args))

    def _get_lines(self, location):
        """Return a list of lines for a lication that can be a file or
        a url. If path/url doesn't exist, returns an empty list"""
        try: # This is dirty, but OK I think. both net and file ops raise IOE
            if location.startswith(("http://", "https://")):
                fp = urllib.urlopen(location)
                return [e.strip() for e in fp.read().split('\n')
                        if e and not e.isspace()]
            else:
                fp = open(location)
                return [e.strip() for e in fp.readlines()
                        if e and not e.isspace()]
        except IOError:
            print "Couldn't load %s" % location
            return []
