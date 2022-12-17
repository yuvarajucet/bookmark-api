from dbController.userDBController import getInfoForForgetPassword
from schemas.user import userForgetPasswordSchema
import smtplib
from email.message import EmailMessage


def sendVerificationEmail(user):
    sendVerificationEmail = sendUserVerificationLink(user.email,user.userVerificationToken,user.username)
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


def sendUserVerificationLink(email:str,Vkey:str,username:str):
    print("http://127.0.0.1:8000/api/v1/user/verifyuser?email={0}&Vkey={1}".format(email,Vkey))
    url = "http://127.0.0.1:8000/api/v1/user/verifyuser?email={0}&Vkey={1}".format(email,Vkey)
    #htmlTemplate = generateVerifyUserAccountHTMLEmailTemplate(url,username)
    #email sending with html template process here.
    return {
        "status":True
    }

def sendForgetEmailToUser(userData:userForgetPasswordSchema):
    getDataFromDB = getInfoForForgetPassword(userData.email)
    if getDataFromDB != None:
        if getDataFromDB["status"]:
            url = "http://127.0.0.1:8000/api/v1/user/forgetpassword?email={0}&vToken={1}".format(userData.email,getDataFromDB["data"])
            #htmlTemplate = generateForgetPasswordEmailTemplate(url)
            # email sending with html template process here
            print("http://127.0.0.1:8000/api/v1/user/forgetpassword?email={0}&vToken={1}".format(userData.email,getDataFromDB["data"]))
            return {
                "status_code":getDataFromDB["status_code"],
                "status":True,
                "message":"Verification email sent!"
            }
        return {
            "status_code":getDataFromDB["status_code"],
            "status":False,
            "message":getDataFromDB["message"], 
            "exception":getDataFromDB["exception"]
        }

def generateForgetPasswordEmailTemplate(url):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body{
                margin:0;
                padding:0;
            }
            .container {
                position: relative;
                top:0px;
                left:50%;
                transform: translate(-50%,0);
                background-color: rgb(255, 255, 255);
                width: 90%;
                height: 90%;
                text-align: center;
                box-shadow: 5px 5px 5px rgb(44, 44, 44);
            }
            span{
                font-size: 30px;
            }
            .button {
                position: relative;
                left:50%;
                top:0px;
                transform: translate(-50%,0);
                color: white;
                background-color: blueviolet;
                width: fit-content;
                text-align: center;
                padding:10px;
                font-size: 20px;
                border-radius: 10px;
            }
            a:nth-child(1) {
                color:aliceblue;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-text">
                <span>Hi</span>,
                forget your password
            </div>
            <div class="button">
                <a href="{0}">forget password</a>
            </div>
            if you don't see button please click here <a href="{1}">click here</a>
            <div class="info">
                if you don't do this request please secure your account.
            </div>
        </div>
    </body>
    </html>
    '''.format(url,url)

def generateVerifyUserAccountHTMLEmailTemplate(url,username):
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body{
                margin:0;
                padding:0;
            }
            .container {
                position: relative;
                top:0px;
                left:50%;
                transform: translate(-50%,0);
                background-color: rgb(255, 255, 255);
                width: 90%;
                height: 90%;
                text-align: center;
                box-shadow: 5px 5px 5px rgb(44, 44, 44);
            }
            span{
                font-size: 30px;
            }
            .button {
                position: relative;
                left:50%;
                top:0px;
                transform: translate(-50%,0);
                color: white;
                background-color: blueviolet;
                width: 80px;
                text-align: center;
                padding:10px;
                font-size: 20px;
                border-radius: 10px;
            }
            a:nth-child(1) {
                color:aliceblue;
                text-decoration: none;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header-text">
                <span>Hi</span> {0},
                welcome to bookmarking please verify your account.
            </div>
            <div class="button">
                <a href="{1}">verify</a>
            </div>
            if you don't see button please click here <a href="{2}">click here</a>
        </div>
    </body>
    </html>
    '''.format(username,url,url)
