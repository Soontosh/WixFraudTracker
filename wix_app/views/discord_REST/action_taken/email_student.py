from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import Invoice
from django.http import JsonResponse
import traceback
from django.core.exceptions import ObjectDoesNotExist
from difflib import SequenceMatcher
from wix_app.views.discord_REST.action_taken.action_utilities import action_utilities
from wix_app.views.discord_REST.encode_jwt import encode_jwt
from wix_app.views.discord_REST.decode_jwt import decode_jwt

rest_Utilities = rest_utilities()
action_Utilities = action_utilities()

@api_view(["POST"])
def email_student(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    #try
    raw_json_data = json.loads(request.body)
    json_data = decode_jwt(raw_json_data)
    student_email = json_data["student_email"]
    student_name = json_data["student_name"]
    #except

    action_Utilities.notify_student(student_email, student_name)
    return Response(encode_jwt({"data": "success"}), status=200)