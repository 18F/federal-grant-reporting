from django.test import TestCase
from django.urls import resolve
from fac.views import homepage


class HomepageTest(TestCase):

    def test_root_url_resolves_to_homepage_view(self):
        found = resolve('/')
        self.assertEqual(found.func, homepage)
