from schemas.user import userRegisterSchema
from models.model import conn,users

def createUser(userData:userRegisterSchema):
    try:
        if not emailIsPresent(userData.email):
            conn.execute(users.insert().values(
                userid = userData.id,
                username = userData.username,
                email = userData.email,
                password = userData.password,
                apikey = userData.apikey,
                userVerificationToken = userData.userVerificationToken,
                isVerified = userData.isVerified,
                userForgetVkey = userData.userForgetVkey
            ))
            return createUserResponse(True,"Registration Success",None)
        else:
            return createUserResponse(False,"Email already exists",None)
    except Exception as e:
        return createUserResponse(False,"Someting went wrong!",e)

def createUserResponse(status:bool,message:str,exception:any):
    return {
        "status":status,
        "message":message,
        "exception":exception
    }

def emailIsPresent(email:str) -> bool:
    isEmailPresent = False
    emailList = conn.execute(users.select().where(users.c.email == email)).fetchall()
    if len(emailList):
        isEmailPresent = True
    return isEmailPresent

