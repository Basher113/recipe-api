from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client

class TestAdmin(TestCase):
    """Testing for Admin"""

    def setUp(self):
        """Set up for admin testing"""
        self.admin_user = get_user_model().objects.create_superuser(email="admin@example.com", password="test123")
        self.client = Client()
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(email="test@exmaple.com", password="test123", name="test")

    def test_render_user_info(self):
        """Tests to check if user list is rendered correctly"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)


    def test_edit_user_page(self):
        """Test the edit user page works."""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
 
        self.assertEqual(res.status_code, 200)

    def test_edit_user_page(self):
        """Test the add user page works."""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
 
        self.assertEqual(res.status_code, 200)