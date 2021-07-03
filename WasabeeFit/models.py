from django.db import models
from django.contrib.auth.models import User
from wasabee import settings  
import stripe
stripe.api_key = settings.STRIPE_API_KEY

# Create your models here.

class Coach(models.Model): 

    name = models.CharField(max_length=100)
    fullname = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics')
    bio = models.TextField()

class Product(models.Model):

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics')
    price = models.IntegerField()



class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    stripe_customer_id = models.CharField(max_length=120)

    # Add additional fields you want to add to the customer profile
     