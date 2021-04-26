from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomUser(models.Model):
    userChoice = (
        ('CUS', 'Customer'),
        ('VEN', 'Vendor'),
        ('WHO', 'Wholesaler'),
        ('DEL', 'Delivery'),
        # ('OTH', 'Other'),
    )
    user = models.OneToOneField(User, related_name='customUser', on_delete=models.CASCADE)
    role = models.CharField(max_length=3, choices=userChoice)
    contact = models.CharField(max_length = 10, null=True, blank=True)
    otp = models.CharField(max_length=4, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=6, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.role

