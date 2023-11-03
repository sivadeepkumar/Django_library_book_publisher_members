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
# from .models import Customer_details
import stripe   
stripe.api_key = settings.STRIPE_SECRET_KEY
from urllib.parse import unquote
from bookmanagement.urls import Bookviewset
from rest_framework.authtoken.models import Token
from django.urls import reverse
from library.views import CustomPermission
from django.views.decorators.cache import cache_page
from .services import DebitCardPaymentView,get_data_from_database,email_sent
import logging
logger = logging.getLogger(__name__)


def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': "This URL's wont have an Views or Logic's Applied"
    })

def cache(request):
    caches = get_data_from_database()
    return JsonResponse({'cache':caches})

def debit_card_payment_view(request, pk):
    payment_list = Payment.objects.filter(borrowing=pk)
    print(payment_list)
    for each in payment_list:
        if each.payment_status == "SUCCESS" :
            return JsonResponse({"Payment status":"Already You Did that and it is succeed"})

    try:
        print('again')
        view = DebitCardPaymentView.as_view()
        return view(request, pk)
    except Exception as e:
        logger.error(f'Error processing debit card payment: {e}')
    return view(request, pk)


def success(request,pk):
    payment = Payment.objects.get(pk=pk)
    payment.payment_status = 'SUCCESS'
    payment.save()
    print(payment.id,pk)
    logger.info(f'Payment ID {payment.id} marked as successful')
    return JsonResponse({'status': 'Payment Succeded'})



def cancel(request,pk):
    payment = Payment.objects.get(pk=pk)
    payment.payment_status = 'FAILED'
    payment.save()
    print(payment.id,pk)
    return JsonResponse({'status': 'Payment Cancelled'})



