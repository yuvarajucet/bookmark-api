from fastapi import FastAPI
from routes.user import user
from routes.admin import admin
from routes.userSettings import userSettings
from routes.bookmark import bookmark

app = FastAPI()

app.include_router(admin)
app.include_router(user)
app.include_router(userSettings)
app.include_router(bookmark)

@app.get('/')
def demoAPI():
    return {
        "Message":"Welcome to bookmarker API"
    }