from django.db import models
from django.contrib.auth.models import User
from wasabee import settings  # <- Change to match your main app name
import stripe
stripe.api_key = settings.STRIPE_API_KEY

# Create your models here.


class CustomerProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    stripe_customer_id = models.CharField(max_length=120)

    # Add additional fields you want to add to the customer profile