import time
from typing import Dict
import jwt
from decouple import config

JWT_SECRET = config("JWT_SECRET_KEY")
JWT_ALGORITHM = config("JWT_ALGORITHM")

def token_response(email:str,token:str):
    return {
        "user_email":email,
        "authorization_token":token,
        "token_type":"bearer"
    }

def signJWT(userId:str,email:str) -> Dict[str,str]:
    exptime = time.time() + 600
    payload ={
        "userId":userId,
        "email":email,
        "expires":exptime
    }

    token = jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)
    return token_response(token)

def decodeJWT(token:str) -> dict:
    try:
        decoded_token = jwt.decode(token,JWT_SECRET,algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            return None
    except:
        return {}