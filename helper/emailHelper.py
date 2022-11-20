from dbController.userDBController import getInfoForForgetPassword
from schemas.user import userForgetPasswordSchema


def sendUserVerificationLink(email:str,Vkey:str):
    print("http://127.0.0.1:8000/api/v1/user/verifyuser?email={0}&Vkey={1}".format(email,Vkey))
    return {
        "status":True
    }

def sendForgetEmailToUser(userData:userForgetPasswordSchema):
    getDataFromDB = getInfoForForgetPassword(userData.email)
    if getDataFromDB != None:
        if getDataFromDB["status"]:
            print("http://127.0.0.1:8000/api/v1/user/forgetpassword?email={0}&vToken={1}".format(userData.email,getDataFromDB["data"]))
            return {
                "status":True,
                "message":"Verification email sent!"
            }
        return {
            "status":False,
            "message":getDataFromDB["message"],
            "exception":getDataFromDB["exception"]
        }