from django.test import TestCase


class FACTest(TestCase):

    def test_fac_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'fac.html')
