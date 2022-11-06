import time
from typing import Dict
import jwt

JWT_SEcret = 'deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f'
alog = 'HS256'


def token_response(token:str):
    return {
        "token":token
    }

def signJWT(userId:str) -> Dict[str,str]:
    expTime = time.time()+600
    print("Current Time : ",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

    payload = {
        "userId":userId,
        "expires":expTime
    }
    token = jwt.encode(payload,JWT_SEcret,algorithm = alog)
    return token_response(token)



def decodeJWT(token:str) -> dict:
    try:
        decoded_token = jwt.decode(token,JWT_SEcret,algorithms = [alog])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}