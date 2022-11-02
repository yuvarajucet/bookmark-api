from fastapi import FastAPI,status,HTTPException
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime,timedelta


SECRET_KEY = "abcdefghijklmnopqrstuvwxyz12][ui"

ALGORITHM = "HS256"

class Token(BaseModel):
    access_token:str
    token_type:str

app = FastAPI()

def createAccessToken(data:dict):
    toEncode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=5)
    toEncode.update({"exp":expire})
    encoded_jwt = jwt.encode(toEncode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt

@app.get("/gettoken")
async def getToken():
    data = {
        'info':'yuvi secrect',
        'from': 'garuda'
    }
    token = createAccessToken(data)
    return {'access_token':token}

@app.get("/verifyToken")
async def verifyToken(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token"
        )