from django.urls import path
from django.views.generic.base import View
from . import views 

urlpatterns = [
    path('',views.index, name='index'),
    path('index',views.index, name='index.html'),
    path('subscription', views.subscription, name='subscription.html'),
    path('success_payment', views.success_payment, name='success_payment.html'),
    path('cancelled_payment', views.cancelled_payment, name='cancelled_payment.html'),
    path('timetable', views.timetable, name='timetable.html')
    ]