from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'




# # Inside apps.py
# from django.apps import AppConfig

# class YourAppConfig(AppConfig):
#     name = 'products'

#     def ready(self):
#         import products.signals  # Add this line




