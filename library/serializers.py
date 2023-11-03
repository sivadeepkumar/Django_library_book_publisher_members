from rest_framework import serializers
from .models import * 
from .views import *
from products.models import *
from rest_framework import serializers
from .models import CustomUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book 
        fields = '__all__'
        
class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields ='__all__'

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

# from django.contrib.auth import get_user_model
# from rest_framework import serializers

# User = get_user_model()

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}


# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(**validated_data)

#         otp = self.generate_otp()
#         self.store_otp_in_sessions(email, otp,request)
        
#         try:
#             email = validated_data['email']
#             subject = 'Welcome to our Meet and We are Heartly expecting your presents in organization'
#             from_email = 'sivadeepkumar3@gmail.com'
#             recipient_list = [email]
            
#             # Load the HTML template
#             html_template = get_template('email_send_context.html')
#             context = {'variable_name': 'value', 'otp': otp}  # Include OTP in the context
#             html_content = html_template.render(context)

#             # Create the EmailMultiAlternatives object
#             msg = EmailMultiAlternatives(subject, 'Thank you for joining our community.', from_email, recipient_list)
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()
#             return user
#         except Exception as e:
#             print(f"An error occurred while sending email: {e}")
#         return user
    
#     def generate_otp(self):
#         return ''.join([str(random.randint(0, 9)) for i in range(6)])

#     def store_otp_in_sessions(self, email, otp, request):
#         request.session['email'] = email
#         request.session['otp'] = otp


# class CustomerdetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer_details
#         fields = '__all__'


# from rest_framework import serializers
# from .models import CustomUser

# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}


# class userSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = User 
#         fields = '__all__'


# class UserDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserDetails
#         fields = '__all__'
