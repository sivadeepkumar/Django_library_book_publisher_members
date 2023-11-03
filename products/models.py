from django.db import models
from library.models import *


class Payment(models.Model):
    borrowing = models.ForeignKey(Borrowing,on_delete=models.CASCADE)
    price = models.IntegerField()
    payment_status = models.CharField(max_length=12)
    payment_by = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.payment_by} : {self.borrowing} : {self.payment_by}'

# class Token(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     key = models.CharField(max_length=40)

#     def __str__(self) -> str:
#         return self.key
    
# import secrets
# def generate_token():
#     return secrets.token_hex(20)

# class Customer_details(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self) -> str:
#         return self.stripe_customer_id
    

# from django.contrib.auth.models import AbstractUser
# from djstripe.models import Customer
# from django.utils.translation import gettext as _

# class CustomUser(AbstractUser):
#     stripe_customer = models.OneToOneField(
#         Customer, null=True, blank=True, on_delete=models.CASCADE)
    
#     groups = models.ManyToManyField(
#         Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
#     user_permissions = models.ManyToManyField(
#         Permission, verbose_name=_('user permissions'), blank=True, related_name='customuser_set')



# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     price = models.IntegerField(default=0) # cents 

#     def __str__(self) -> str:
#         return self.name

