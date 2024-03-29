import requests
from json import load
from os import environ

class rest_utilities:
    def __init__(self) -> None:
        pass

    def check_access_token(self, acc_token: str) -> bool:
        session = requests.Session()
        session.headers = {'Content-Type': 'application/json'}
        session.headers.update({'Authorization': acc_token})
        response = session.post(url='https://www.wixapis.com/apps/v1/bi-event').json()
        if response["message"] == "":
            return False
        
        #Try and get the sample user's id, if it exists, the token is valid
        with open("/wix_app/JSONTemplates/query_member.json") as json_file: json_data = load(json_file)
        json_data["id"] = environ['MEMBER_ID']

        #return whether or not the wix servers are down, surface errors in discord
        response_data = session.post(url='https://www.wixapis.com/apps/v1/bi-event').json()

        if response_data["members"] == []:
            return False

        return True