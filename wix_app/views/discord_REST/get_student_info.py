"""The final stage, getting the "fraudulent" student's info"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import Invoice
from django.http import JsonResponse
import traceback
from django.core.exceptions import ObjectDoesNotExist
from difflib import SequenceMatcher
from wix_app.views.discord_REST.decode_jwt import decode_jwt
from wix_app.views.discord_REST.encode_jwt import encode_jwt

rest_Utilities = rest_utilities()

@api_view(["GET"])
def get_student_info(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    try:
        #Extract JSON data and list
        raw_json_data = json.loads(request.body)
        json_data = decode_jwt(raw_json_data)
        invoice_number = json_data["invoice_number"]
    except json.JSONDecodeError:
        return Response("Malformed Data", status=400)
    except KeyError:
        return Response("Malformed Data", status=400)
    except ValueError:
        return Response("Malformed Offense Counts", status=400)
    except TypeError:
        return Response("Malformed Offense Counts", status=400)
    except Exception:
        return Response("Error", status=400)
    
    try:
        invoice = Invoice.objects.get(invoice_number=invoice_number)
        invoice_data = {
            'customer_full_name': invoice.contact_name,
            'customer_email': invoice.contact_email,
            'student_name': invoice.student_name,
            'student_email': invoice.student_email if invoice.student_email else None,
            'total': invoice.total,
            'preview_link': invoice.preview_link,
            'offenses': invoice.offenses
        }
    except Invoice.DoesNotExist:
        pass # Handle the case where the invoice_number does not exist
    #except Exception:
    #    pass # Handle general error

    return JsonResponse(encode_jwt(invoice_data), safe=False)