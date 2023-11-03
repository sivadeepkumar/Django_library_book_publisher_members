from django.http import JsonResponse

from library.models import *
from rest_framework import viewsets,permissions 
from django.shortcuts import render,redirect
from .serializers import BookSerializer,PublisherSerializer,BorrowingSerializer,PaymentSerializer  #,CustomerdetailsSerializer,userSerializers
from products.models import *
from django.http import HttpResponse
response = HttpResponse()
from rest_framework import generics
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response

class CustomPermission(permissions.BasePermission):
    def has_permission(self, request,view):
        if request.user and request.user.is_authenticated:
            if request.user.is_superuser:
                return True
            return (request.method in ['GET', 'HEAD', 'OPTIONS'])
        return False

class CreateUserView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

class Bookviewset(viewsets.ModelViewSet):
    queryset = Book.objects.all()  
    serializer_class = BookSerializer 

    # authentication_classes = [TokenAuthentication] 
    permission_classes = [CustomPermission]

class Publisherviewset(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()  
    serializer_class = PublisherSerializer 

    # authentication_classes = [TokenAuthentication] 
    permission_classes = [CustomPermission]

class PaymentSerializerviewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [CustomPermission]

class Borrowingviewset(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = BorrowingSerializer

    # authentication_classes = [TokenAuthentication] 
    permission_classes = [CustomPermission]

    def get_queryset(self):
        user_id = self.request.user.id
        user =self.request.user
        print(user_id,user)

        if user.is_authenticated:
            if not user.is_superuser:
                return Borrowing.objects.filter(member = user_id)
        return Borrowing.objects.all()


# service layer 
    def list(self, request):
        borrowings = self.get_queryset()
        for borrowing in borrowings:
            if borrowing.returned_date:
                borrowed_days = (borrowing.returned_date - borrowing.borrowed_date).days
            else:
                today = datetime.date.today()
                borrowed_days = (today - borrowing.borrowed_date).days
            if borrowed_days > 7:
                borrowing.overdue_charge = borrowed_days * 1
                borrowing.save()
        return super().list(request)


import random

def generate_otp():
    str_ = ""
    for i in range(6):
        str_ += str(random.randint(0,9))
    print(str_)
    print(type(str_))
    return ''.join([str(random.randint(0, 9)) for i in range(6)])



def overdue_zero(request):
    Borrow = Borrowing.objects.all()
    for i in Borrow:
        i.overdue_charge = 0
        i.save()
    return redirect('Borrowingviewset-list')



def logout(request):
    response.delete_cookie('jwt_token')
    jwt_token = response.cookies['jwt_token']
    try:
        print(jwt_token)
    except:
        print('Jwt Token is deleted')
    return HttpResponse('Deleted')

 
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
# views.py

import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView



from datetime import timedelta
import random
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CustomUser
from .serializers import CustomUserSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for i in range(6)])

            # Store OTP in sessions
            request.session['email'] = email
            request.session['otp'] = otp
            request.session.set_expiry(timedelta(minutes=1).seconds)

            user = CustomUser(email=email, is_active=False)
            user.set_password(password)
            user.save()
            # Send email
            try:
                subject = 'Welcome to our Meet and We are Heartly expecting your presents in organization'
                from_email = 'sivadeepkumar3@gmail.com'
                recipient_list = [email]
                html_template = get_template('email_send_context.html')
                context = {'variable_name': 'value', 'otp': otp}
                html_content = html_template.render(context)

                msg = EmailMultiAlternatives(subject, 'Thank you for joining our community.', from_email, recipient_list)
                msg.attach_alternative(html_content, "text/html")
                msg.send()

                return Response({'message': 'OTP sent successfully. Check your email for OTP.'}, status=status.HTTP_200_OK)

            except Exception as e:
                print(f"An error occurred while sending email: {e}")
                return Response({'message': 'An error occurred while sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404

class OTPVerificationView(APIView):
    def post(self, request):
        email = request.session.get('email')
        otp = request.data.get('otp')

        # Retrieve OTP from session
        stored_otp = request.session.get('otp')
        
        if otp == stored_otp:
            # OTP is correct, activate the user
            try:
                user = CustomUser.objects.get(email=email)
                user.is_active = True
                user.save()
                return Response({'message': 'User verified successfully.'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)



#{
#    "email": "sivadeepkumar3@gmail.com"
#}

class OTPResendView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        try:
            user = CustomUser.objects.get(email=email, is_active=False)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist or has already been verified.'}, status=status.HTTP_400_BAD_REQUEST)

        otp = ''.join([str(random.randint(0, 9)) for i in range(6)])

        request.session['email'] = email
        request.session['otp'] = otp
        request.session.set_expiry(timedelta(minutes=1).seconds)

        
        try:
            subject = 'Welcome to our Meet and We are Heartly expecting your presents in organization'
            from_email = 'sivadeepkumar3@gmail.com'
            recipient_list = [email]
            html_template = get_template('email_send_context.html')
            context = {'variable_name': 'value', 'otp': otp}
            html_content = html_template.render(context)

            msg = EmailMultiAlternatives(subject, 'Thank you for joining our community.', from_email, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return Response({'message': 'New OTP sent successfully. Check your email for OTP.'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"An error occurred while sending email: {e}")
            return Response({'message': 'An error occurred while sending email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







import schedule
import time

# Global flag to control scheduling
scheduled_task_enabled = False

def start_scheduled_task():
    global scheduled_task_enabled
    scheduled_task_enabled = True
    schedule.every(1).minutes.do(print_hello)

def stop_scheduled_task():
    global scheduled_task_enabled
    scheduled_task_enabled = False

def print_hello():
    print("hello world")

def run_scheduler():
    while True:
        if scheduled_task_enabled:
            schedule.run_pending()
        time.sleep(1)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def start_scheduler(request):
    start_scheduled_task()
    return JsonResponse({'message': 'Scheduler started'})

@csrf_exempt
def stop_scheduler(request):
    stop_scheduled_task()
    return JsonResponse({'message': 'Scheduler stopped'})