from pydantic import BaseModel, Field,EmailStr

class User(BaseModel):
    name:str
    email:str
    password:str

class PostSchema(BaseModel):
    id:int = Field(default=None)
    title:str = Field(...)
    content:str = Field(...)

    class Config:
        schema_extra ={
            "example":{
                "title":"Securign fastapi with JWT",
                "content":"In this will help"
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "yuvaraj",
                "email": "yuvaraj@gmail.com",
                "password": "test@123"
            }
        }


class loginSchema(BaseModel):
    email:EmailStr = Field(...)
    password:str = Field(...)

    class Config:
        schema_extra ={
            "example":{
                "email":"yuvaraj@gmail.com",
                "password":"test@123"
            }
        }