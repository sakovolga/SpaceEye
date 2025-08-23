from django.test import TestCase
from django.contrib.auth.models import User
from django.db import IntegrityError
from ..models import Favorite


class FavoriteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )

    def test_favorite_creation(self):
        favorite = Favorite.objects.create(
            user=self.user,
            favorite_type='apod',
            title='Test APOD',
            description='Test description',
            image_url='https://example.com/image.jpg',
            api_data={'test': 'data'}
        )
        self.assertEqual(str(favorite), f"{self.user.username} - Test APOD")

    def test_unique_constraint(self):
        Favorite.objects.create(
            user=self.user,
            favorite_type='apod',
            title='Test APOD',
            image_url='https://example.com/image.jpg',
            api_data={'test': 'data'}
        )

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(
                user=self.user,
                favorite_type='apod',
                title='Another title',
                image_url='https://example.com/image.jpg',
                api_data={'other': 'data'}
            )

    def test_cascade_delete(self):
        Favorite.objects.create(
            user=self.user,
            favorite_type='apod',
            title='Test APOD',
            image_url='https://example.com/image.jpg',
            api_data={'test': 'data'}
        )

        user_id = self.user.id
        self.user.delete()

        self.assertEqual(Favorite.objects.filter(user_id=user_id).count(), 0)