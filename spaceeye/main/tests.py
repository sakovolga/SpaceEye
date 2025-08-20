from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock


class SpaceEyeTestCase(TestCase):
    def setUp(self):
        self.client = Client()

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
        response = self.client.get(reverse('main:mars_rover'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mars Rover Photos')
