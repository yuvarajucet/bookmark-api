from fastapi import APIRouter

userSettings = APIRouter(
    prefix='/api/v1/usersettings',
    tags=['userSettings'],
    responses={404:{"Description":"Not found"}}
)

@userSettings.post("/update-user-settings",tags=['userSettings'])
def updateUserSettings():
    pass

@userSettings.get("/getusersettings",tags=['userSettings'])
def getUserSettings():
    pass