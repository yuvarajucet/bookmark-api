import uuid
import hashlib

def generateUserID():
    return str(uuid.uuid4())

def generateVerificationToken():
    return str(uuid.uuid4())

def generateForgetToken():
    return str(uuid.uuid4())

def passwordHasher(plainPassword):
    result = hashlib.md5(plainPassword.encode())
    return result.hexdigest()

