from pydantic import BaseModel,Field,EmailStr

class userRegisterSchema(BaseModel):
    id:str = Field(default=None)
    username:str = Field(...)
    email:EmailStr = Field(...)
    password:str = Field(...)
    apikey:str = Field(default=None)
    userVerificationToken:str = Field(default=None)
    isVerified:str = Field(default=0)
    userForgetVkey:str = Field(default=None)

    class Config:
        schema_extra = {
            "example":{
                "username":"testUser",
                "email":"demo@gmail.com",
                "password":"***********",
            }
        }

class userLoginSchema(BaseModel):
    email:EmailStr = Field(...)
    password:str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "email":"demo@gmail.com",
                "password":"*********"
            }
        }


class bookmarkSchema(BaseModel):
    id:str = Field(...)
    category:str = Field(...)
    url:str = Field(...)
    label:str = Field(...)
    icon:str = Field(default=None)

    class Config:
        schema_extra = {
            "example":{
                "category":"Search Engine",
                "url":"google.com",
                "label":"Google"
            }
        }