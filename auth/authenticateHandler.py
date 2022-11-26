import time
from typing import Dict
import jwt

JWT_SECRET = "deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f"
JWT_ALGORITHM = "HS256"

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