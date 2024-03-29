"""Contains function to decode incoming JWT data"""

import jwt
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from pytz import UTC

#Load environment variables
load_dotenv(find_dotenv('.env'))

def decode_jwt(raw_data):
    print("raw data type: " + str(type(raw_data)))
    jwt_data = jwt.decode(jwt=raw_data,
                key = os.getenv("JWT_KEY"),
                algorithms=["HS256"])
    
    return jwt_data

#issue is w/ what is being passed in, it is a dictionary type and not a string!