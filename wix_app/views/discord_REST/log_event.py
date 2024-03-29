from wix_app.models import *
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import Invoice
from django.http import JsonResponse
import traceback
from django.core.exceptions import ObjectDoesNotExist
from difflib import SequenceMatcher
from datetime import datetime
from pytz import UTC
from wix_app.views.discord_REST.decode_jwt import decode_jwt
from wix_app.views.discord_REST.encode_jwt import encode_jwt


rest_Utilities = rest_utilities()

@api_view(["POST"])
def log_event(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)

    json_data_raw = json.loads(request.body)
    json_data = decode_jwt(json_data_raw)
    error_message = json_data["error_message"]
    json_data_json = json_data["json_data"]

    #Error always equal to True for now as it is only used for error logging
    newLog = EventLog(timestamp = datetime.now(UTC), error=True, error_message = error_message, json_data = json_data_json, event_type="DISCORD_BOT")
    newLog.save()

    return Response(newLog.id, status=200)