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
    <body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <img width="60" src="#" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="padding:0 35px;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">You have
                                            requested to reset your password</h1>
                                        <span
                                            style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
                                            We cannot simply send you your old password. A unique link to reset your
                                            password has been generated for you. To reset your password, click the button to verify
                                        </p>
                                        <a href="{0}"
                                            style="background:#6862d5;text-decoration:none !important; font-weight:500; margin-top:35px; color:#fff;text-transform:uppercase; font-size:14px;padding:10px 24px;display:inline-block;border-radius:50px;">Reset
                                            Password</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong>www.bookmarking.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
        </table>
    </body>
    </html>
    '''.format(url)

def generateVerifyUserAccountHTMLEmailTemplate(url,username):
    return '''
    <html>
    <body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
        <tr>
            <td>
                <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                    align="center" cellpadding="0" cellspacing="0">
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <img width="60" src="#" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="padding:0 35px;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Please verify your account</h1>
                                        <span
                                            style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
                                           Hi {0} ,Please click the below button to verify your user account.
                                        </p>
                                        <a href="{1}"
                                            style="background:#6862d5;text-decoration:none !important; font-weight:500; margin-top:35px; color:#fff;text-transform:uppercase; font-size:14px;padding:10px 24px;display:inline-block;border-radius:50px;">
                                            Verify</a>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong>www.bookmarking.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
        </table>
    </body>
    </html>
    '''.format(username,url)


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