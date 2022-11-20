from pydantic import BaseModel,Field

class userRegisterSchema(BaseModel):
    id:str = Field(default=None)
    username:str = Field(...)
    email:str = Field(...)
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
    email:str = Field(...)
    password:str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "email":"demo@gmail.com",
                "password":"*********"
            }
        }


# class bookmarkSchema(BaseModel):
#     id:str = Field(...)
#     category:str = Field(...)
#     url:str = Field(...)
#     label:str = Field(...)
#     icon:str = Field(default=None)

#     class Config:
#         schema_extra = {
#             "example":{
#                 "category":"Search Engine",
#                 "url":"google.com",
#                 "label":"Google"
#             }
#         }

class userForgetPasswordSchema(BaseModel):
    email:str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "email":"demo@gmail.com"
            }
        }

class forgetPasswordSchema(BaseModel):
    email:str = Field(...)
    vToken:str = Field(...)
    newPassword:str = Field(...)
    conformPassword:str = Field(...)

    class Config:
        schema_extra = {
            "example":{
                "email":"demo@gmail.com",
                "vToken":"password reset token",
                "newPassword":"******",
                "conformPassword":"******"
            }
        }