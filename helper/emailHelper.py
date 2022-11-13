

def sendUserVerificationLink(email:str,Vkey:str):
    print("http://127.0.0.1:8000/api/v1/user/verifyuser?email={0}&Vkey={1}".format(email,Vkey))
    return {
        "status":True,
    }