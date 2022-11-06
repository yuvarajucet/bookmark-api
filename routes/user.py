from fastapi import APIRouter,Body,Depends
from config.db import conn
from models.index import users
from schemas.index import *
from auth.index import *

user = APIRouter()

posts =[]

userDb = []

def checkUser(data:loginSchema):
    for user in userDb:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@user.post("/login",tags=['user'])
async def login(user:loginSchema = Body(...)):
    if checkUser(user):
        return {
         "authorization_token":signJWT(user.email)["token"],
         "user":user.email,
         "token_type":"Bearer"
        }
    return {
        "error" : "user name or password is wrong!"
    }


@user.post("/register",tags=['user'])
async def newUser(user: UserSchema = Body(...)):
    userDb.append(user)
    return {
        "status":"Register Success"
    }


@user.post("/post",dependencies=[Depends(JWTBearer())],tags=['Post'])
async def addPost(post:PostSchema) -> dict:
    post.id = len(posts) +1
    posts.append(post.dict())
    return {
        "data":"Post success"
    }


@user.get("/get-user",tags=["userList"])
async def getUser():
    return {
        "users": userDb
    }


@user.get("/get-post/{id}",dependencies=[Depends(JWTBearer())],tags=["postlist"])
async def getPost(id:int):
    if id > len(posts):
        return {
            "status":"No post Yet"
        }
    for post in posts:
        if(post["id"] == id):
            return {
                "posts": post
            }




#with data Base : 
@user.get("/")
async def read_data():
    return conn.execute(users.select()).fetchall()


@user.get("/{id}")
async def read_data(id:int):
    return conn.execute(users.select().where(users.c.id == id)).fetchall()

@user.post("/")
async def write_data(user:User):
    conn.execute(users.insert().values(
        name = user.name,
        email = user.email,
        password = user.password
    ))
    return conn.execute(users.select()).fetchall()

@user.put("/{id}")
async def update_data(id:int,user:User):
    conn.execute(users.update().values(
        name = user.name,
        email = user.email,
        password = user.password
    ).where(users.c.id == id))
    return conn.execute(users.select()).fetchall()


@user.delete("/",dependencies=[Depends(JWTBearer())])
async def delete_data(id:int):
    conn.execute(users.delete().where(users.c.id == id))
    return conn.execute(users.select()).fetchall()