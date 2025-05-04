from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("users:create")
TOKEN_USER_URL = reverse("users:token")


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""
    
    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        params = {
            "email": "test@example.com",
            "password": "test123",
            "name": "test"
        }
        res = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=params["email"])

        self.assertTrue(user.check_password(params["password"]))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        params = {
            "email": "test@example.com",
            "password": "test123",
            "name": "test"
        }
        # existing user
        exist_user = get_user_model().objects.create_user(**params)

        res = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short_error(self):
        """Test an error is returned when password is less than 5 chars."""
        params = {
            "email": "test@example.com",
            "password": "test",
            "name": "test"
        }

        res = self.client.post(CREATE_USER_URL, params)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        exist_user = get_user_model().objects.filter(email=params["email"]).exists()
        self.assertFalse(exist_user)

    def test_token_generated_successful(self):
        """Test for generating a token to a valid users"""
        users_info = {
            "email": "test@example.com",
            "password": "good_password",
            "name": "test_name"
        }

        get_user_model().objects.create_user(**users_info)

        payload = {
            "email": users_info["email"],
            "password": users_info["password"]
        }

        res = self.client.post(TOKEN_USER_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
