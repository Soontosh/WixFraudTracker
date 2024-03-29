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
def get_student_discord_ids(request):
    if not rest_Utilities.check_access_token(request.headers.get('Authorization')):
        return Response("Forbidden", status=403)
    
    try:
        #Extract JSON data and list
        print("check 1")
        raw_json_data = json.loads(request.body)
        print("raw_json_data")
        print(raw_json_data)
        json_data = decode_jwt(raw_json_data)
        print("json_data")
        print(json_data)
        student_names = json_data["student_names"]
        discord_names = json_data["discord_members"]
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

    #Create dictionary w/ list comprehension
    nickname_dictionary = {name[1]: (find_most_similar_nickname(name[0], discord_names), name[0]) for name in student_names}

    print("nickname_dictionary: ")
    print(nickname_dictionary)

    #Return dictionary as JSON Response
    return JsonResponse(encode_jwt(nickname_dictionary), safe=False)

#Helper function to find the most similar nickname
def find_most_similar_nickname(real_name, discord_names):
    """
    Function to find the most similar nickname for a given real name from the list of nicknames.
    
    Args:
    real_name (str): The real name for which the most similar nickname needs to be found.
    discord_nicknames (list): The list of nicknames to compare with the real name.
    
    Returns:
    str: The most similar nickname for the given real name.
    """
    max_ratio = 0  # Initialize the maximum similarity ratio
    most_similar_nickname = "N/A"  # Default value if no similar nickname is found
    most_similar_id = "N/A"  # Default value if no similar nickname is found


    for id in discord_names.keys():  # Iterate through the list of nicknames
        nickname = discord_names[id]
        similarity_ratio = SequenceMatcher(None, real_name, nickname).ratio()  # Calculate the similarity ratio
        if similarity_ratio > max_ratio:  # Update the most similar nickname if a higher similarity ratio is found
            max_ratio = similarity_ratio
            most_similar_nickname = nickname
            most_similar_id = id
    return (most_similar_id, most_similar_nickname)  # Return the most similar id and nickname