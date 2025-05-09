from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Star, Order

class StarModelTest(TestCase):
    def test_create_star(self):
        star = Star.objects.create(
            name="TestStar",
            constellation="TestCon",
            magnitude=2.0,
            ra=12.5,
            dec=55.5
        )
        self.assertEqual(star.name, "TestStar")


class OrderFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='testpass')
        self.star = Star.objects.create(
            name="OrderStar",
            constellation="OrderCon",
            magnitude=1.5,
            ra=5.5,
            dec=44.4
        )

    def test_login_required_redirect(self):
        response = self.client.get('/order/')
        self.assertEqual(response.status_code, 302)  # should redirect to login

    def test_create_order_logged_in(self):
        self.client.login(username='user1', password='testpass')
        response = self.client.post('/order/', {
            'star': self.star.id,
            'name_given': 'MyStar'
        })
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.name_given, 'MyStar')
        self.assertEqual(order.user.username, 'user1')

