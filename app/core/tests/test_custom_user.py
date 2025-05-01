"""Testing for Custom User"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTest(TestCase):

    def test_new_user(self):
        """Tests for new users"""
        User = get_user_model()
        user = User.objects.create_user(email="test@example.com", password="test123")

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("test123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="test123")
    
    def test_normalise_email(self):
        sample_emails = [
            ["test1@example.com", "test1@example.com"],
            ["Test2@example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@EXAMPLE.com", "test4@example.com"],
            ["test5@example.COM", "test5@example.com"]
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email=email, password="test123")
            self.assertEqual(user.email, expected)

    def test_admin_user(self):
        """"Tests for admin users"""
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="admin@example.com", password="test123")

        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)