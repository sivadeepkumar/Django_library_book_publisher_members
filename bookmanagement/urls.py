from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from library.views import *
from products.views import *
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls import handler404, handler500
from library.views import CreateUserView
import debug_toolbar
from library.views import *

router = DefaultRouter()
router.register(r'books',Bookviewset,basename='Bookviewset')
router.register(r'publish',Publisherviewset,basename='Publisherviewset')
router.register(r'borrow',Borrowingviewset,basename='Borrowingviewset')
router.register(r'payment',PaymentSerializerviewset,basename='PaymentSerializerviewset')
# Multiple Threading
# Customers and Billing Subscribtion

# custom - validation(Regex)
# data flow and Er diagram
# pytest  - To implement in this project
# rockets screens  
# payment : link 
# Mixins - multiple inhertent 
# Nginx
# Expiring Jwt token

# Error Handling and Logging:  Implement error handling mechanisms to provide informative error responses. Set up logging to capture relevant information.
# Data Caching:  Implement data caching strategies to improve API performance.
# Email service:Implement an email greeting message for when a user is created.

# Format of template should be change to img and OTP 15 mins to store , One time use and 15 mins it should leave 
# weather api integer temp,humidity and Air Quanlity test 
# schedule any process for a specific time (Timeinterval) and 
# increption and decreption to secure the details encode and decode 

# blueprint

def custom404(request, exception=None):
    return JsonResponse({
        'status_code': 404,
        'error': 'The resource was not found'
    })

def custom500(request, exception=None):
    return JsonResponse({
        'status_code': 500,
        'error': 'Check the Server Whether it is running or not'
    })


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),   # all api's are triggered by api via router.register
    path('api/borrow/<int:pk>/payment/', debit_card_payment_view, name='debit_card_payment_view'),
    path('success/<int:pk>/',success, name='success'),
    path('cancel/<int:pk>/', cancel, name='cancel'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/',logout,name='logout'),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/otp_verification/', OTPVerificationView.as_view(), name='otp_verification'),
    path('api/otp_resend/', OTPResendView.as_view(), name='otp_resend'),
    path('cache/',cache,name='cache'),
    path('__debug__/',include(debug_toolbar.urls)),
    path('weather/', include('weather.urls')),
    path('start_scheduler/', start_scheduler, name='start_scheduler'),
    path('stop_scheduler/', stop_scheduler, name='stop_scheduler'),
]


handler404 = custom404
handler500 = custom500




# services:
#   web:
#     build: .
#     ports:
#       - "8000:5000"
#     volumes:
#       - .:/code
#       - logvolume01:/var/log
#     depends_on:
#       - redis
#   redis:
#     image: redis
# volumes:
#   logvolume01: {}