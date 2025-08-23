import json
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.cache import cache
from ..models import Favorite
from ..views import get_apod_data


class MainViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cache.clear()

    def test_index_view_anonymous(self):
        url = reverse("main:index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "main/index.html")
        self.assertIn("nasa_data", resp.context)

    @patch("main.views.get_apod_data")
    def test_index_view_with_date_and_authenticated(self, mock_apod):
        self.client.login(username="testuser", password="testpass")
        mock_apod.return_value = {"url": "http://image.jpg", "title": "Test"}
        url = reverse("main:index") + "?date=2024-05-01"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue("is_favorited" in resp.context)

    @patch("main.views.requests.get")
    def test_get_apod_data_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"media_type": "image", "url": "http://test.jpg"}
        mock_resp.raise_for_status = lambda: None
        mock_get.return_value = mock_resp

        data = get_apod_data("2024-01-01")
        self.assertIn("url", data)
        self.assertEqual(data["source"], "apod")

    def test_api_data_ajax_invalid_type(self):
        url = reverse("main:api_data_ajax") + "?type=unknown"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"error": "Invalid API type"})

    @patch("main.views.get_mars_rover_data")
    def test_api_data_ajax_mars_rover(self, mock_rover):
        mock_rover.return_value = {"photos": [], "source": "mars_rover"}
        url = reverse("main:api_data_ajax") + "?type=mars_rover&sol=1000&rover=curiosity"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("mars_rover", resp.json()["source"])

    def test_add_to_favorites_apod(self):
        self.client.login(username="testuser", password="testpass")
        url = reverse("main:add_to_favorites")
        payload = {
            "type": "apod",
            "data": {"title": "Pic", "explanation": "desc", "url": "http://img.jpg"},
        }
        resp = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"success": True, "action": "added"})
        self.assertEqual(Favorite.objects.count(), 1)

    def test_remove_from_favorites(self):
        fav = Favorite.objects.create(
            user=self.user,
            favorite_type="apod",
            image_url="http://img.jpg",
            title="Pic",
            description="desc",
            api_data={"url": "http://img.jpg"},
        )
        self.client.login(username="testuser", password="testpass")
        url = reverse("main:remove_from_favorites")
        payload = {"type": "apod", "image_url": fav.image_url}
        resp = self.client.post(url, data=json.dumps(payload), content_type="application/json")
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {"success": True, "action": "removed"})
        self.assertEqual(Favorite.objects.count(), 0)

    def test_favorites_list_filter(self):
        Favorite.objects.create(
            user=self.user,
            favorite_type="mars_rover",
            image_url="http://img.jpg",
            title="Pic",
            description="desc",
            api_data={},
        )
        self.client.login(username="testuser", password="testpass")
        url = reverse("main:favorites") + "?type=mars_rover"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "main/favorites.html")
        self.assertEqual(len(resp.context["favorites"]), 1)

    def test_register_view_success(self):
        url = reverse("main:register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
        }
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(username="newuser").exists())

