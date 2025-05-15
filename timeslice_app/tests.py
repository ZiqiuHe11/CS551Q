from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Timeslice, Order

class TimesliceModelTest(TestCase):
    def test_timeslice_creation(self):
        timeslice = Timeslice.objects.create(name="Test Slice", price=9.99)
        self.assertEqual(timeslice.name, "Test Slice")

class HomeViewTest(TestCase):
    def test_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='testpass')
        self.timeslice = Timeslice.objects.create(name="Test Slice", price=10)

    def test_add_to_order(self):
        self.client.login(username='tester', password='testpass')
        url = reverse('add_to_order', args=[self.timeslice.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302) 
