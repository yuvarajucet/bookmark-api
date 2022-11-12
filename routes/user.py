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

@user.get("/createdb",tags=['admin'])
async def index():
    resp = createTables()
    return resp



@user.post("/register",tags=['user'])
async def register(user: userRegisterSchema = Body(...)):
    user.id = generateUserID()
    user.userVerificationToken = generateVerificationToken()
    user.password = passwordHasher(user.password)
    print(user)
    registerStatus = createUser(user)
    response_message = {
        "status":registerStatus["status"],
        "message":registerStatus["message"],
        "error":registerStatus["exception"]
    }
    return response_message