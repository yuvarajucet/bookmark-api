from fastapi import APIRouter,Body,Depends,Response
from schemas.user import userRegisterSchema,userLoginSchema,userForgetPasswordSchema,forgetPasswordSchema
from helper.userHelper import generateUserID,generateVerificationToken,passwordHasher
from helper.emailHelper import sendVerificationEmail,sendForgetEmailToUser
from dbController.userDBController import createUser,userLogin,verifyUser,updateUserPassword
from auth.athenticateUser import JWTBearer

user = APIRouter(
    prefix='/api/v1/user',
    tags=['user'],
    responses={404:{"Description":"Not found"}}
)


@user.get("/",tags=['user'])
async def index():
    return {
        "message":"User router working"
    }

@user.post("/register",tags=['user'])
async def register(resp:Response,user: userRegisterSchema = Body(...)):
    user.id = generateUserID()
    user.userVerificationToken = generateVerificationToken()
    user.password = passwordHasher(user.password)
    response = createUser(user)
    emailStatus = {}
    if response["status"]:
        resp.status_code = response["status_code"]
        emailStatus = sendVerificationEmail(user)
    return {
        "register_status":response,
        "verification_email":emailStatus
    }


@user.post("/login",tags=['user'])
async def login(resp:Response,user:userLoginSchema = Body(...)):
    user.password = passwordHasher(user.password)
    response = userLogin(user)
    resp.status_code = response["status_code"]
    return response


# @user.get("/resendverificationmail",tags=['user'])
# async def resendUserVerificationLink():
#     pass

@user.get("/verifyuser",tags=['user'])
async def verifyUserRegistration(resp:Response,email:str,Vkey:str):
    response = verifyUser(email,Vkey)
    resp.status_code = response["status_code"]
    return response


@user.post("/sendforgetpasswordlink",tags=['user'])
async def sendForgetPasswordLink(resp:Response,userData:userForgetPasswordSchema):
    response = sendForgetEmailToUser(userData)
    resp.status_code = response["status_code"]
    return response

@user.post("/forgetpassword",tags=['user'])
async def forgetPassword(resp:Response,newPassword:forgetPasswordSchema):
    if newPassword.newPassword == newPassword.conformPassword:
        response = updateUserPassword(newPassword)
        resp.status_code = response["status_code"]
        return response
    return {
        "status_code":"200",
        "status":False,
        "message":"New password and conform password mismatch!"
    }

@user.put("/update-user-profile",dependencies=[Depends(JWTBearer())], tags=['user'])
async def updateUserProfile():
    return {
        "message":"Not implemented"
    }

@user.delete("/delete-user",dependencies=[Depends(JWTBearer())],tags=['user'])
async def deleteUser():
    return {
        "message":"Not Implemented"
    }