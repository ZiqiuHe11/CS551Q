from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class TimeSlice(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    historical_date = models.DateField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} ({self.historical_date})"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    timeslices = models.ManyToManyField(TimeSlice)  
    order_date = models.DateTimeField(auto_now_add=True)  
    total_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)  

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        
        if not self.total_price:  
            self.total_price = sum(timeslice.price for timeslice in self.timeslices.all()) 
        super(Order, self).save(*args, **kwargs)  


# Create your models here.
