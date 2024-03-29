"""Extract more information regarding events. 
Can be used in tandem with  'get_events' to extract all necessary information."""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from wix_app.views.discord_REST.REST_utilities import rest_utilities
import json
from wix_app.models import EventLog
from django.http import JsonResponse
import traceback
from wix_app.views.discord_REST.decode_jwt import decode_jwt

rest_Utilities = rest_utilities()

@api_view(["GET"])
def get_event_data(request):
    #Ensure access token is valid, if not, return 403
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    #Load and extract JSON data
    try:
        #Extract JSON data and list
        raw_json_data = json.loads(request.body)
        json_data = decode_jwt(raw_json_data)
        id_list = json_data["ids"]

        #Convert list to have integers instead of strings
        int_id_lists = [int(i) for i in id_list]
    except json.JSONDecodeError:
        return Response("Malformed Data", status=400)
    except KeyError:
        return Response("Malformed Data", status=400)
    except ValueError:
        return Response("Malformed IDs", status=400)
    except TypeError:
        return Response("Malformed IDs", status=400)
    except Exception:
        return Response("Error", status=400)
    
    #Dictionary to store results
    result_dict = {}

    #Iterate through each ID
    for id in id_list:
        try:
            event_log = EventLog.objects.get(id=id)
            # Extract required information
            info = {
                "Event Type": event_log.event_type,
                "Event Timestamp": event_log.timestamp,
                "Associated Parent's Name": event_log.associated_invoice.contact_name,
                "Associated Parent's Email": event_log.associated_invoice.contact_email,
                "Associated Product": event_log.associated_invoice.status,
                "Associated Invoice Link": event_log.associated_invoice.preview_link
            }

            #If the associated student email exists, add to dictionary
            if event_log.associated_invoice.student_email:
                info["Associated Student Name"] = event_log.associated_invoice.student_name

            result_dict[str(id)] = info
        except EventLog.DoesNotExist:
            #Log the following data
            #result_dict[str(id)] = {"Error": "Event Log not found for the provided ID"}
            print("err 1")
            pass
        except AttributeError:
            #Log the following data
            #result_dict[str(id)] = {"Error": "Associated Parent's Email, Name, Product, or Invoice Link is null"}
            print("err 2")
            pass
        except Exception as e:
            #Log the following data
            #result_dict[str(id)] = {"Error": f"An unexpected error occurred: {str(e)}"}
            print("err 3: " + str(traceback.format_exc()))
            pass

    return JsonResponse(result_dict, safe=False)