from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials


from auth.user import decodeJWT

class JWTBearer(HTTPBearer):
    def __init__(self,auto_error: bool = True):
        super(JWTBearer,self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer,self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                print(credentials.scheme)
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verifyJWT(credentials.credentials):
                raise HTTPException(status_code=403,detail="Invalid token or expired token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403,detail="Invalid Authorization Token")




    def verifyJWT(self,jwtToken:str) -> bool:
        isTokenValid:bool = False
        try: 
            payload = decodeJWT(jwtToken)
        except:
            payload = None
        if payload:
            isTokenValid = True

        return isTokenValid