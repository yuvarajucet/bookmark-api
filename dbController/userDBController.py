from schemas.user import userRegisterSchema
from models.model import conn,users,createRequiredTable

def createUser(userData:userRegisterSchema):
    try:
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
        response_message = {
            "status":True,
            "message":"Registration success",
            "exception":None
        }
        return response_message
    except Exception as e:
        response_message = {
            "status":False,
            "message":"Registration failed someting went wrong",
            "exception": e
        }
        return response_message



def createTables():
    resp = createRequiredTable()
    return resp