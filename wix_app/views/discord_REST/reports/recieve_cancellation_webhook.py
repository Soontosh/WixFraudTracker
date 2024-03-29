from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import *
from django.http import JsonResponse
from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from pytz import UTC

#Load environment variables
load_dotenv(find_dotenv('.env'))

@api_view(["POST"])
def recieve_cancellation_webhook(request):

    #Malformed data if not possible
    raw_data_str = request.body.decode('utf-8')
    print("Raw data string")
    print(raw_data_str)

    #Forbidden if not possible

    decodedData = jwt.decode(jwt=raw_data_str,
            key = os.getenv("JWT_KEY"),
            algorithms=["HS256"], options={"verify_signature": False})
    
    cancellationLog = CancellationLogs(timestamp = datetime.now(UTC), json_data = str(decodedData))
    cancellationLog.save()

    return Response("Success", status=200)