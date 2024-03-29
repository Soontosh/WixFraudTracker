"""Contains function to decode incoming JWT data"""

import jwt
from dotenv import load_dotenv, dotenv_values, find_dotenv
import os
from pytz import UTC

#Load environment variables
load_dotenv(find_dotenv('.env'))

def encode_jwt(raw_data) :
    jwt_data = jwt.encode(payload=raw_data,
                key = os.getenv("JWT_KEY"),
                algorithm="HS256")
    
    return jwt_data