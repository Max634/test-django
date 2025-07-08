from django.test import TestCase

class HomeViewTestCase(TestCase):
    def test_home_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_template_content(self):
        response = self.client.get('/')
        self.assertContains(response, "<title>")  # Or any string you have in your template
