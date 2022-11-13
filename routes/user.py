from fastapi import APIRouter,Body,Depends
from schemas.user import userRegisterSchema,userLoginSchema
from helper.userHelper import generateUserID,generateVerificationToken,passwordHasher
from helper.emailHelper import sendUserVerificationLink
from dbController.userDBController import createUser

user = APIRouter(
    prefix='/api/v1/user',
    tags=['user'],
    responses={404:{"Description":"Not found"}}
)


def sendVerificationEmail(user:userRegisterSchema):
    sendVerificationEmail = sendUserVerificationLink(user.email,user.userVerificationToken)
    if(sendVerificationEmail["status"]):
        emailStatus = {
            "status":True,
            "message":"Verification email sent to {0}".format(user.email)
        }
    else:
        emailStatus = {
            "status":False,
            "message":"We facing problem in sending verification email"
        }
    return emailStatus

@user.get("/",tags=['user'])
async def index():
    return {
        "message":"User router working"
    }

@user.post("/register",tags=['user'])
async def register(user: userRegisterSchema = Body(...)):
    user.id = generateUserID()
    user.userVerificationToken = generateVerificationToken()
    user.password = passwordHasher(user.password)
    response = createUser(user)
    emailStatus = {}
    if response["status"]:
        emailStatus = sendVerificationEmail(user)
    return {
        "register_status":response,
        "verification_email":emailStatus
    }


@user.post("/login",tags=['user'])
async def login(user:userLoginSchema = Body(...)):
    pass

@user.get("/verifyuser",tags=['user'])
async def verifyUserRegistration():
    pass

@user.get("/resendverificationmail",tags=['user'])
async def resendUserVerificationLink():
    pass

@user.get("/sendforgetpasswordlink",tags=['user'])
async def sendForgetPasswordLink():
    pass

@user.get("/verify-forget-link",tags=['user'])
async def verifyForgetLink():
    pass

@user.post("/forgetpassword",tags=['user'])
async def forgetPassword():
    pass

@user.put("/update-user-profile",tags=['user'])
async def updateUserProfile():
    pass

@user.delete("/delete-user",tags=['user'])
async def deleteUser():
    pass