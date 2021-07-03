from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from .models import Coach
from .models import Product
from .models import CustomerProfile
import stripe
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from wasabee import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
stripe.api_key = settings.STRIPE_API_KEY

# Create your views here.

PRODUCTS_STRIPE_PRICING_ID = {
    'sub_standart': 'price_1Hp8wWFZ98jXoTtbriINZCHx',
    'sub_pro': 'price_1Hp8xIFZ98jXoTtbkVoDRIyz',
    'sub_ultimate': 'price_1Hp8y1FZ98jXoTtbduULkPDL',

    'dumbell_chd_10': 'price_1HwXfZFZ98jXoTtbx5hBAYZq',
    'herba_mango_shake_500g': 'price_1HwY2ZFZ98jXoTtbEAqKS6mg',
    'sweatshirt01' : 'price_1HwZm2FZ98jXoTtbtZLZZAnG',
    'gnc_protien' : 'price_1HwZpwFZ98jXoTtbUTcHyvNt',
    'yoga_mat' : 'price_1HwZtiFZ98jXoTtbn6UXos1B'
    'barbell_10kg' 'price_1HwmIFFZ98jXoTtbUscuP6zf'
}

@login_required
@csrf_exempt
def create_stripe_checkout_session(request, product_name):

    try:

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer=request.user.customerprofile.stripe_customer_id,
            client_reference_id=request.user.id,
            metadata={'product_name': product_name, },
            line_items=[
                {'price': PRODUCTS_STRIPE_PRICING_ID[product_name], 'quantity': 1, },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success_payment?session_id={CHECKOUT_SESSION_ID}',
           cancel_url='http://localhost:8000/cancelled_payment',        )

        return JsonResponse({'id': checkout_session.id})

    except Exception as e:
        print(e)
        raise SuspiciousOperation(e)


@require_POST
@csrf_exempt
def stripe_webhook_paid_endpoint(request):

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    # Try to validate and create a local instance of the event
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_SIGNING_SECRET)
    except ValueError as e:
        # Invalid payload
        return SuspiciousOperation(e)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return SuspiciousOperation(e)

  # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        checkout_session = event['data']['object']
        # Make sure is already paid and not delayed
        if checkout_session.payment_status == "paid":
            _handle_successful_payment(checkout_session)

    # Passed signature verification
    return HttpResponse(status=200)

def _handle_successful_payment(checkout_session):
    # Define what to do after the user has successfully paid
    pass

def subscription(request):
    return render(request, "subscription.html")

def timetable(request):
    return render(request, "timetable.html")



def success_payment(request):
    return render(request, "success_payment.html")


def cancelled_payment(request):
    return render(request, "cancelled_payment.html")


def index(request):

    coachs = Coach.objects.all()
    
    return render(request, "index.html", {'coachs' : coachs})

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

def shop(request):

    products = Product.objects.all()
    
    return render(request, "shop.html", {'products' : products})
