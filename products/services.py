from products.models import Payment
from typing import Any
from django.shortcuts import render,redirect
from django.conf import settings
from django.views import View
from django.http import JsonResponse,HttpResponse, Http404
from django.views.generic import TemplateView
from library.models import *
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
from urllib.parse import unquote
from bookmanagement.urls import Bookviewset
from rest_framework.authtoken.models import Token
from django.urls import reverse
from library.views import CustomPermission


import logging

logger = logging.getLogger(__name__)

# ... (your other code)



class DebitCardPaymentView(APIView):
    permission_classes = [CustomPermission]

    def get(self, request, pk):
        try:
            borrowing_list = Borrowing.objects.filter(id=pk)
            borrowing = borrowing_list[0]
            charge = borrowing_list[0].overdue_charge
            borrowing_member = borrowing_list[0].member

            payment = Payment.objects.create(
                borrowing=borrowing,
                price=charge,
                payment_status='Pending',
                payment_by=borrowing_member,
            )
            payment_id = payment.id

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": "inr",
                            "unit_amount": int(charge * 100),
                            "product_data": {
                                "name": borrowing_member,
                            },
                        },
                        "quantity": 1,
                    }
                ],
                customer_email='sivadeepkumar3@gmail.com',
                metadata={"borrowing_id": borrowing.id},
                mode="payment",
                success_url=request.build_absolute_uri(reverse('success', kwargs={'pk': payment_id})),
                cancel_url=request.build_absolute_uri(reverse('cancel', kwargs={'pk': payment_id}))
            )
            

            return JsonResponse({'Payment_link': checkout_session.url})
        
        except Http404 as e:
            logger.exception("HTTP 404 Error: %s", e)
            return JsonResponse({'error': str(e)}, status=404)
        
        except Exception as e:
            logger.exception("An error occurred: %s", e)
        return JsonResponse({'error': str(e)}, status=500)



def email_sent():
    try:
        email = 'sivadeepkumar199@gmail.com'
        # Your email sending code here
        subject = 'Welcome to our site'
        message = 'Thank you for joining our community.'
        from_email = 'sivadeepkumar3@gmail.com'  # Replace with your email address
        recipient_list = [email]
        logger.info('Sending email to %s', email)
        send_mail(subject, message, from_email, recipient_list, 'email_send_context.html')
        logger.info('Email sent successfully to %s', email)

    except Exception as e:
        logger.exception('An error occurred while sending email: %s', e)
        print(f"An error occurred while sending email: {e}")
    



from django.views.decorators.cache import cache_page
from django.core.cache import cache

def get_data_from_database():
    data = cache.get('siva')
    if data is None:
        data = 'HUNT' 
        cache.set('siva', data, 15)  
    return data

