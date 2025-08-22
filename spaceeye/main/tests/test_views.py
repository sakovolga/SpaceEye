from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch, Mock


class SpaceEyeTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_index_page_loads(self):
        response = self.client.get(reverse('main:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Astronomy Picture of the Day')

    @patch('requests.get')
    def test_apod_with_date(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            'title': 'Test Space Image',
            'url': 'http://example.com/space.jpg',
            'explanation': 'Test explanation',
            'date': '2023-01-01',
            'media_type': 'image'
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        response = self.client.get(reverse('main:index'), {'date': '2023-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Space Image')

    def test_mars_rover_page(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('main:mars_rover'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mars Rover Photos')

    def test_mars_rover_page_redirects_when_not_authenticated(self):
        response = self.client.get(reverse('main:mars_rover'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/') or
                        response.url.startswith('/login/'))