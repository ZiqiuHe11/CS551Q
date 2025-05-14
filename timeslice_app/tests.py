from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Star, Order

class AdminDashboardTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser('admin', 'admin@test.com', 'pass123')
        self.client = Client()
    
    def test_admin_dashboard_access(self):
        self.client.login(username='admin', password='pass123')
        response = self.client.get('/admin-dashboard/')
        self.assertEqual(response.status_code, 200)
