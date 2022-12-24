import uvicorn
from fastapi import FastAPI
from routes.user import user
from routes.admin import admin
from routes.userSettings import userSettings
from routes.bookmark import bookmark
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(admin)
app.include_router(user)
app.include_router(bookmark)
app.include_router(userSettings)


origins = [
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def demoAPI():
    return {
        "Message":"Welcome to bookmarker API"
    }

if __name__ == "__main__":
    uvicorn.run(app=app)
