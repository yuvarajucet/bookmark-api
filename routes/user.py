from fastapi import APIRouter,Body,Depends
from schemas.user import userRegisterSchema,userLoginSchema
from helper.userHelper import generateUserID,generateVerificationToken,passwordHasher
from dbController.userDBController import createUser,createTables

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
async def register(user: userRegisterSchema = Body(...)):
    pass

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