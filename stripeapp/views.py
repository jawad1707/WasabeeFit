from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your views here.

@receiver(post_save, sender=User)
def _on_update_user(sender, instance, created, **kwargs):

    if created:  # If a new user is created

        # Create Stripe user
        customer = stripe.Customer.create(
            email=instance.email,
            name=instance.get_full_name(),
            metadata={
                'user_id': instance.pk,
                'username': instance.username
            },
            description='Created from Django',
        )

        # Create profile
        profile = CustomerProfile.objects.create(user=instance, stripe_customer_id=customer.id)
        profile.save()
