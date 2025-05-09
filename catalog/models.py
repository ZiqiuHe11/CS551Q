from django.db import models
from django.contrib.auth.models import User

class Star(models.Model):
    name = models.CharField(max_length=100)
    constellation = models.CharField(max_length=100)
    magnitude = models.FloatField()
    ra = models.FloatField(help_text="Right Ascension")
    dec = models.FloatField(help_text="Declination")

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'In Cart'),
        ('paid', 'Paid, Awaiting Confirmation'),
        ('confirmed', 'Confirmed & Named'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star = models.ForeignKey(Star, on_delete=models.CASCADE)
    name_given = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=19.99)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name_given} → {self.star.name} ({self.status})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('user', 'User'), ('admin', 'Admin')], default='user')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


