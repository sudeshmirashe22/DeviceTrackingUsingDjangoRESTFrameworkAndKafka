# from django.shortcuts import render
# from .models import *
# from django.http import JsonResponse

# # Create your views here.
# def index(request):
#     return render(request, 'index.html')

# def get_data(request):
#     latest_data = LocationUpdate.objects.latest('timestamp')
#     return JsonResponse({
#         'latitude' : latest_data.latitude,
#         'longitude' : latest_data.longitude,
#         'timestamp' : latest_data.timestamp
#     })

# tracker/views.py
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from confluent_kafka import Producer
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from tracker.models import LocationUpdate

# JsonResponse({
#         "message":  "Hello to you too"
#     })

@csrf_exempt
def hello(request):
    if request.method == "POST":
        device_id = request.data.get('device_id')
        print(device_id)
        return  JsonResponse({
        "message":  "POST method"
      })
    else:
        return JsonResponse({
        "message":  "GET method"
      })

def index(request):
    return render(request, 'index.html')

def get_data(request):
    latest_data = LocationUpdate.objects.latest('timestamp')
    return JsonResponse({
        "device_id":  latest_data.device_id,
        'latitude' : latest_data.latitude,
        'longitude' : latest_data.longitude,
        'timestamp' : latest_data.timestamp
    })

# Configure logger
logger = logging.getLogger(__name__)

# Kafka Producer Configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)

class LocationUpdateAPI(APIView):
    def post(self, request):
        # Extract data
        device_id = request.data.get('device_id')
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')

        # Basic validation
        if not all([device_id, latitude, longitude]):
            return JsonResponse(
                {"error": "Missing required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Prepare payload
        payload = {
            "device_id": device_id,
            "latitude": latitude,
            "longitude": longitude
        }
        print(payload)

        try:
            # Send to Kafka
            producer.produce(
                topic='location_updates',
                value=json.dumps(payload).encode('utf-8')
            )
            producer.flush()
            return JsonResponse(
                {"message": "Location sent to Kafka."},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"Kafka Producer Error: {str(e)}")
            return JsonResponse(
                {"error": "Failed to send location to Kafka."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
