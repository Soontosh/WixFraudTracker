from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import EventLog
from django.http import JsonResponse

rest_Utilities = rest_utilities()

@api_view(["GET"])
def get_events(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    try:
        data = json.loads(request.body)
        start_date = data["start-date"]
        end_date = data["end-date"]
    except json.JSONDecodeError as e:
        #Handle
        return Response("Malformed Data", status=400)
    except KeyError as e:
        #Handle
        return Response("Malformed Data", status=400)
    except Exception as e:
        #Handle
        return Response("Error", status=400)

    filtered_logs = list(EventLog.objects.filter(timestamp__range=(start_date, end_date), error=False).values())

    return JsonResponse(filtered_logs, safe=False)