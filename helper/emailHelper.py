from dbController.userDBController import getInfoForForgetPassword
from schemas.user import userForgetPasswordSchema
import os
from dotenv import load
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

load()

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
    rootUrl = os.getenv('FRONTEND_ROOT_URL')
    verificationEndPoint = os.getenv('USER_VERIFICATION_ENDPOINT')
    url = "{0}{1}?email={2}&Vkey={3}".format(rootUrl,verificationEndPoint,email,Vkey)
    htmlTemplate = generateVerifyUserAccountHTMLEmailTemplate(url,username)
    emailStatus = sendEmailToUser(email,htmlTemplate,'Email Verification')
    if(emailStatus["email_status"]):
        return {
            "status":True
        }
    return {
        "status":False
    }


def sendForgetEmailToUser(userData:userForgetPasswordSchema):
    getDataFromDB = getInfoForForgetPassword(userData.email)
    if getDataFromDB != None:
        if getDataFromDB["status"]:
            vToken = getDataFromDB["data"]
            rootUrl = os.getenv('FRONTEND_ROOT_URL')
            verificationEndPoint = os.getenv('FROGET_PASSWORD_ENDPOINT')
            url = "{0}{1}?email={2}&vToken={3}".format(rootUrl,verificationEndPoint,userData.email,vToken)
            htmlTemplate = generateForgetPasswordEmailTemplate(url)
            emailStatus = sendEmailToUser(userData.email,htmlTemplate,'Forget Password')
            if(emailStatus["email_status"]):
                return {
                    "status_code":200,
                    "status":True,
                    "message":"Email send to your registered email address"
                }
            return {
                 "status_code":200,
                 "status":False,
                 "message":"Facing problem in sending email"
            }
        return {
            "status_code":getDataFromDB["status_code"],
            "status":False,
            "message":getDataFromDB["message"], 
            "exception":getDataFromDB["exception"]
        }

def generateForgetPasswordEmailTemplate(url):
    return '''
    <html>
    <body>
        <div class="container" style="position:relative;top:0px;left:50%;transform:translate(-50%,0);background-color:rgb(255,255,255);width:90%;height:90%;text-align:center;box-shadow: 5px 5px 5px rgb(44, 44, 44);">
            <div class="header-text">
                <span style="font-size:30px">Hi</span>,
                forget your password
            </div>
            <div class="button" style="position:relative;left:50%;top:0px;transform:translate(-50%,0);color:white;background-color:blueviolet;width:80px;text-align:center;padding:10px;font-size:20px;border-radius:10px">
                <a href="{0}">forget password</a>
            </div>
            if you don't see button please click here <a style="color:aliceblue;text-decoration:none" href="{1}">click here</a>
            <div class="info">
                if you don't do this request please secure your account.
            </div>
        </div>
    </body>
    </html>
    '''.format(url,url)

def generateVerifyUserAccountHTMLEmailTemplate(url,username):
    return '''
    <html>
    <body>
        <div class="container" style="position:relative;top:0px;left:50%;transform:translate(-50%,0);background-color:rgb(255,255,255);width:90%;height:90%;text-align:center;box-shadow: 5px 5px 5px rgb(44, 44, 44);">
            <div class="header-text">
                <span style="font-size:30px">Hi</span> {0},
                welcome to bookmarking please verify your account.
            </div>
            <div class="button" style="position:relative;left:50%;top:0px;transform:translate(-50%,0);color:white;background-color:blueviolet;width:80px;text-align:center;padding:10px;font-size:20px;border-radius:10px">
                <a href="{1}">verify</a>
            </div>
            if you don't see button please click here <a style="color:aliceblue;text-decoration:none" href="{2}">click here</a>
        </div>
    </body>
    </html>
    '''.format(username,url,url)


def sendEmailToUser(userEmail,htmlTemplate,subject):
    adminEmail = os.getenv('ADMIN_EMAIL')
    adminPassword = os.getenv('ADMIN_PASSWORD')

    email_message = MIMEMultipart()
    email_message['From'] = adminEmail
    email_message['To'] = userEmail
    email_message['Subject'] = subject

    email_message.attach(MIMEText(htmlTemplate,"html"))
    email_string = email_message.as_string()

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com",465,context=context) as server:
            server.login(adminEmail,adminPassword)
            server.sendmail(adminEmail,userEmail,email_string)
            return {
                "email_status":True
            }
    except Exception as e:
        return {
            "email_status":False,
            "Exception":e
        }