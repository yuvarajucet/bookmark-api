from schemas.user import userRegisterSchema,userLoginSchema
from models.model import conn,users
from auth.authenticateHandler import signJWT

# Register user
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
            return createResponse(True,"Registration Success",None)
        else:
            return createResponse(False,"Email already exists",None)
    except Exception as e:
        return createResponse(False,"Someting went wrong!",e)


# user Login
def userLogin(userData:userLoginSchema):
    try:
        userList = conn.execute('SELECT userid FROM users WHERE email="{0}" AND password="{1}"'.format(userData.email,userData.password)).fetchone()
        if  userList != None and len(userList):
            if(userAccountVerified(userData.email)):
                auth_token = signJWT(userList[0],userData.email)
                data = {
                    "userid":userList[0],
                    "userData":auth_token
                }
                return createResponse(True,"Login success",None,data)
            else:
                return createResponse(False,"Please verify your account",None,None)
        else:
            return createResponse(False,"Username or password not found",None)
    except Exception as e : 
        return createResponse(False,"Someting went wrong",e)





# ------------------------  Supporting methods ----------------------------------


# create common structure response to router
def createResponse(status:bool,message:str,exception:any,userData:any = None):
    return {
        "status":status,
        "message":message,
        "exception":str(exception),
        "data":userData
    }

# check account is verified or not
def userAccountVerified(email:str) ->bool:
    isAccountVerified = False
    verificationStatus = conn.execute("SELECT isVerified FROM users WHERE email='{0}'".format(email)).fetchone()
    if verificationStatus != None:
        if(len(verificationStatus)):
            if verificationStatus[0] == True:
                isAccountVerified = True
    return isAccountVerified

# find given email is present or not
def emailIsPresent(email:str) -> bool:
    isEmailPresent = False
    emailList = conn.execute(users.select().where(users.c.email == email)).fetchall()
    if len(emailList):
        isEmailPresent = True
    return isEmailPresent

