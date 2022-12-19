import time
from typing import Dict
import jwt
import os
from dotenv import load

load()

JWT_SECRET = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('HS256')

def token_response(email:str,token:str,exptime):
    return {
        "user_email":email,
        "authorization_token":token,
        "token_type":"bearer",
        "expire":exptime
    }

def signJWT(userId:str,email:str) -> Dict[str,str]:
    exptime = time.time() + 10000
    payload ={
        "userId":userId,
        "email":email,
        "expires":exptime
    }
    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_response(email,token,exptime)

def decodeJWT(token:str) -> dict:
    try:
        decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            return None
    except:
        return {}