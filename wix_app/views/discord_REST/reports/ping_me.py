from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import *
from django.http import JsonResponse
from datetime import datetime, timedelta
from wix_app.views.discord_REST.REST_utilities import rest_utilities
from wix_app.views.discord_REST.decode_jwt import decode_jwt
from wix_app.views.discord_REST.encode_jwt import encode_jwt

rest_Utilities = rest_utilities()

@api_view(["GET"])
def ping_me(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    try:
        #Extract JSON data and list
        raw_json_data = json.loads(request.body)
        json_data = decode_jwt(raw_json_data)
        discord_id = json_data["discord_id"]
    except json.JSONDecodeError:
        return Response("Malformed Data", status=400)
    except KeyError:
        return Response("Malformed Data", status=400)
    except ValueError:
        return Response("Malformed Data - Values", status=400)
    except TypeError:
        return Response("Malformed Data - Values", status=400)
    except Exception:
        return Response("Error", status=400)
    
    if Ping.objects.filter(id=str(discord_id)).exists():
        Ping.objects.filter(id=str(discord_id)).delete()
        return Response(0, status=200)
    else:
        Ping.objects.create(id=str(discord_id))
        return Response(1, status=200)