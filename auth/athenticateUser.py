from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials

from auth.authenticateHandler import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self,auto_error:bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)

    async def __call__(self,request:Request):
        creadentials:HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if creadentials:
            if not creadentials.scheme == "Bearer":
                raise HTTPException(status_code=403,detail={})
            if not self.verifyJWT(creadentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            return creadentials.credentials
        else:
            raise HTTPException(status_code=403,detail="Invalid Authorization token")



    def verifyJWT(self,JWTToken:str) -> bool:
        isTokenValid:bool = False
        try:
            payload = decodeJWT(JWTToken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid