from django.shortcuts import render
import requests
from datetime import datetime
# Create your views here.
from decouple import config
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
API_KEY = config('API_KEY')


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@csrf_exempt
def weather(request):
    try:
        if request.method == 'POST':
            # Get the JSON data from the request body
            body = json.loads(request.body.decode('utf-8'))
            city_name = body.get('city_name')
            # import pdb 
            # pdb.set_trace()
            print(city_name)
            if city_name:

                # The rest of your code remains the same
                url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
                response = requests.get(url).json()
                current_time = datetime.now()
                formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
                city_weather_update = {
                    'city': city_name,
                    'description': response['weather'][0]['description'],
                    'icon': response['weather'][0]['icon'],
                    'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                    'country_code': response['sys']['country'],
                    'wind': 'Wind: ' + str(response['wind']['speed']) + 'km/h',
                    'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                    'time': formatted_time
                }

                context = {'city_weather_update': city_weather_update}
                return JsonResponse(city_weather_update)

            else:
                return JsonResponse({'error': 'City name not provided'}, status=400)

        else:
            return JsonResponse({'error': 'Invalid request method'}, status=405)

    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Internal server error'}, status=500)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def encode_chunk(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        body = json.loads(request.body.decode('utf-8'))
        encode = body.get('encode')
        
        # Check if encode is None or empty
        if encode is None or encode == "":
            return JsonResponse({'message': 'Invalid input'})

        chunk = encode
        encoded_value = 0
        
        for i, char in enumerate(chunk):
            ascii_value = ord(char)
            
            for j in range(8):
                encoded_value |= ((ascii_value >> j) & 1) << (i*8 + j)
        
        return JsonResponse({'encoded_value': encoded_value})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
def decode_chunk(request):
    if request.method == 'POST':
        # Get the JSON data from the request body
        body = json.loads(request.body.decode('utf-8'))
        decode_it = body.get('decode')
        
        # Check if decode_it is None
        if decode_it is None:
            return JsonResponse({'message': 'Invalid input'})
    
        decoded_chars = ""
    
        while decode_it > 0:
            ascii_value = 0
            for j in range(8):
                ascii_value |= ((decode_it) & 1) << j
                decode_it >>= 1

            decoded_chars += chr(ascii_value)
        
        return JsonResponse({'decoded_chars': decoded_chars})


# import schedule
# import time
# from django.http import JsonResponse

# # Define a variable to hold the scheduled job
# timer_job = None
# timer_value = 0

# def start_timer():
#     global timer_job, timer_value  # Use the global variables
    
#     if timer_job is None:
#         # Schedule the task to run every 30 minutes
#         timer_job = schedule.every(1).minutes.do(runtimmer)
#         timer_value = 0
#         print('Interval: STARTED')
#     else:
#         print('Interval already STARTED')

# def pause_timer(value):
#     global timer_value  # Use the global variable
    
#     if timer_job is not None:
#         schedule.cancel_job(timer_job)
#         timer_value = value
#         print(f'Interval: PAUSED at {timer_value}')
#     else:
#         print('Interval is not STARTED')

# def stop_timer():
#     global timer_job, timer_value  # Use the global variables
    
#     if timer_job is not None:
#         schedule.cancel_job(timer_job)
#         timer_job = None  # Reset the variable
#         timer_value = 0
#         print('Interval: STOPPED')
#     else:
#         print('Interval is not STARTED')

# def runtimmer():
#     print(f'Timer: {timer_value}')

# @csrf_exempt
# def control_timer(request):
#     global timer_value
    
#     if request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         action = body.get('action')
#         value = body.get('value')
        
#         if action == 'startTimer':
#             start_timer()
#             return JsonResponse({'message': 'Timer started'})
#         elif action == 'pauseTimer':
#             pause_timer(value)
#             return JsonResponse({'message': f'Timer paused at {value}'})
#         elif action == 'stopTimer':
#             stop_timer()
#             return JsonResponse({'message': 'Timer stopped'})
#         else:
#             return JsonResponse({'error': 'Invalid action'}, status=400)
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=405)    
