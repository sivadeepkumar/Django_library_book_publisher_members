
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from djstripe.models import Customer

# @receiver(post_save, sender=User)
# def create_stripe_customer(sender, instance, created, **kwargs):
#     if created:
#         # Create a customer on Stripe
#         customer = Customer.create(instance)
#         instance.stripe_customer = customer
#         instance.save()
