from schemas.user import userRegisterSchema,userLoginSchema,forgetPasswordSchema
from models.model import conn,users
from helper.userHelper import generateForgetToken,passwordHasher
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
            return createResponse(200,True,"Registration Success",None)
        else:
            return createResponse(200,False,"Email already exists",None)
    except Exception as e:
        return createResponse(500,False,"Someting went wrong!",e)

# user Login
def userLogin(userData:userLoginSchema):
    try:
        userList = conn.execute("SELECT userid FROM users WHERE email='{0}' AND password='{1}'".format(userData.email,userData.password)).fetchone()
        if  userList != None and len(userList):
            if(isUserAccountVerified(userData.email)):
                auth_token = signJWT(userList[0],userData.email)
                data = {
                    "userid":userList[0],
                    "userData":auth_token
                }
                return createResponse(200,True,"Login success",None,data)
            else:
                return createResponse(200,False,"Please verify your account",None,None)
        else:
            return createResponse(200,False,"Username or password is wrong",None)
    except Exception as e : 
        return createResponse(500,False,"Something went wrong",e)

# verify user based on email and verification token
def verifyUser(email,Vkey):
    try:
        if emailIsPresent(email):
            if not isUserAccountVerified(email):
                isValidToken = conn.execute("SELECT userid FROM users WHERE email='{0}' AND userVerificationToken='{1}'".format(email,Vkey)).fetchall()
                if isValidToken != None and len(isValidToken):
                    conn.execute("UPDATE users SET isVerified={0} WHERE email = '{1}' AND userVerificationToken = '{2}'".format(1,email,Vkey))
                    return createResponse(200,True,"User verification Success",None)
                else:
                    return createResponse(200,False,"email and token mismatching",None)
            else:
                return createResponse(200,False,"Account already verified",None)
        else:
            return createResponse(200,False,"Email Not found",None)
    except Exception as e:
        return createResponse(500,False,"Something went wrong",e)



#get forget password details from user data
def getInfoForForgetPassword(email):
    try:
        if emailIsPresent(email):
            forgetToken = generateForgetToken()
            conn.execute("UPDATE users SET userForgetVkey='{0}' WHERE email = '{1}'".format(forgetToken,email))
            return createResponse(200,True,"verification token generated",None,forgetToken)
        return createResponse(200,False,"Email not found",None)
    except Exception as e:
        return createResponse(500,False,'Something went wrong',e)


# update password for user:
def updateUserPassword(userData:forgetPasswordSchema):
    try:
        if(emailIsPresent(userData.email)):
            isValidRequest = conn.execute("SELECT userid FROM users WHERE email='{0}' AND userForgetVkey='{1}'".format(userData.email,userData.vToken)).fetchall()
            if isValidRequest != None and len(isValidRequest):
                hashedPassword = passwordHasher(userData.newPassword)
                conn.execute("UPDATE users SET password='{0}' WHERE userForgetVkey='{1}'".format(hashedPassword,userData.vToken))
                conn.execute("UPDATE users SET userForgetVkey='{0}' WHERE password='{1}'".format(None,hashedPassword))
                return createResponse(200,True,"Password Reset completed",None)
            else:
                return createResponse(401,False,"Email and Verification token expired or mismatch",None)
    except Exception as e:
        return createResponse(500,False,"Something went wrong!",e)

# ------------------------  Supporting methods ----------------------------------
# create common structure response to router
def createResponse(statusCode:int,status:bool,message:str,exception:any,userData:any = None):
    return {
        "status_code":statusCode,
        "status":status,
        "message":message,
        "exception":str(exception),
        "data":userData
    }

# check account is verified or not
def isUserAccountVerified(email:str) ->bool:
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
    if emailList != None and len(emailList):
        isEmailPresent = True
    return isEmailPresent

