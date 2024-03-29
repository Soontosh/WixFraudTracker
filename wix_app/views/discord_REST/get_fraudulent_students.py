"""Using the given parameters, query for students whose parents have not been paying invoices!"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import Invoice
from django.http import JsonResponse
import traceback
from django.core.exceptions import ObjectDoesNotExist
from wix_app.views.discord_REST.decode_jwt import decode_jwt
from wix_app.views.discord_REST.encode_jwt import encode_jwt

rest_Utilities = rest_utilities()

@api_view(["GET"])
def get_fraudulent_students(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    #Load and extract JSON data
    try:
        #Extract JSON data and list
        raw_json_data = json.loads(request.body)
        json_data = decode_jwt(raw_json_data)
        offenses_list = json_data["offenses"]

        offenses_list = [int(i) for i in offenses_list]
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
        #Get the highest number of offenses out of all overdue invoices
        #Also tests to see if any fraudulent students have been detected
        largest_offense = Invoice.objects.filter(status="OVERDUE").order_by('-offenses').first().offenses
        if 3 in offenses_list:
            largest_offense = Invoice.objects.filter(status="OVERDUE").order_by('-offenses').first().offenses

            #Add all numbers between 3 and the largest value to the offenses_list variable
            offenses_list += range(4, largest_offense + 1)
    except AttributeError:
        #Means that no fraudsters can be matched with that number of offenses
        return Response(encode_jwt({"data": None}), status=200)
    
    try:
        # Query the table for rows that meet the specified conditions
        overdue_invoices = Invoice.objects.filter(status="OVERDUE", offenses__in=offenses_list)   
    except ObjectDoesNotExist:
        print("No invoices found with the specified conditions.")
        return Response("No invoices found with the specified conditions", status=400)
    except Exception as e:
        print(f"An error occurred: {e}")
        return Response("Error", status=400)
    
    student_names = {"data": [(invoice.student_name, invoice.invoice_number) for invoice in overdue_invoices]}
    print("towards end?")
    return Response(encode_jwt(student_names), status=200)