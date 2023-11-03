from django.contrib.auth.models import User
import datetime
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
import random

def validate_custom_email(value):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, value):
        raise ValidationError('Invalid email address')
    

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,validators=[validate_custom_email],)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email



# class CustomUserManager(BaseUserManager):

#     def create_user(self, email, password=None,request = None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
        
    #     otp = self.generate_otp()
    #     self.store_otp_in_sessions(email, otp, request)
    #     message = f'Your OTP is {otp}. Please use this OTP to verify your email.'
        
    #     try:
    #         # Your email sending code here
    #         subject = 'Welcome to our site'
    #         from_email = 'sivadeepkumar3@gmail.com'
    #         recipient_list = [email]
    #         send_mail(subject, message, from_email, recipient_list, 'email_send_context.html')
    #         return user
    #     except Exception as e:
    #         print(f"An error occurred while sending email: {e}")

    # def generate_otp(self):
    #     return ''.join([str(random.randint(0, 9)) for i in range(6)])

    # def store_otp_in_sessions(self, email, otp, request):
    #     request.session['email'] = email
    #     request.session['otp'] = otp

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#         return self.create_user(email, password, **extra_fields)



# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     # Normal email which i implemented
#     # email = models.EmailField(uniqueTrue)

#     #This is Regex Implemented email
#     email = models.EmailField(unique=True,validators=[validate_custom_email],)
    
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email


class Publisher(models.Model):
    publisher = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self) -> str:
        return self.publisher


class Book(models.Model):
    title = models.CharField(max_length=100,null=True,blank=True)
    published_by = models.ForeignKey(Publisher,on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    AVAILABLE_CHOICES = [
        ('In-stock', 'In-stock'),
        ('Out-of-stock', 'Out-of-stock'),
    ]

    availability = models.CharField(max_length=12, choices=AVAILABLE_CHOICES, default='In-stock')
    book_count = models.IntegerField(default=1)

    def __str__(self) -> str:
        return f'Title: {self.title}, Author : {self.author}'


class Borrowing(models.Model):
    member = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_date = models.DateField(default=datetime.date.today)
    returned_date = models.DateField(null=True, blank=True)
    overdue_charge = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f'{self.member} , {self.book}'
    

from django.utils import timezone
class OTP(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_value = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def is_expired(self):
        now = timezone.now()
        return (now - self.timestamp).total_seconds() > 15 * 60  # Check if OTP is older than 15 minutes




# class Payment(models.Model):
#     borrowing = models.ForeignKey(Borrowing,on_delete=models.CASCADE)
#     price = models.IntegerField()
#     payment_status = models.CharField(max_length=12)
#     payment_by = models.CharField(max_length=100)

#     def __str__(self) -> str:
#         return f'{self.payment_by} : {self.borrowing} : {self.payment_by}'





# class UserDetails(models.Model):
#     userId = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
#     email = models.EmailField(validators=[validate_custom_email])  
#     phone_number = models.IntegerField()
    
#     IS_STUDENT = [
#         ('B-tech','B-tech'),
#         ('Degree','Degree')
#     ]
#     stream = models.CharField(max_length=40,choices=IS_STUDENT,default=IS_STUDENT[0])

#     def __str__(self) -> str:
#         return self.email
