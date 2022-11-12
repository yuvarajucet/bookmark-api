from fastapi import FastAPI
import uvicorn
from routes.user import user

app = FastAPI()

app.include_router(user)

@app.get('/')
def demoAPI():
    return {
        "Message":"Welcome to bookmarker API"
    }

if __name__ == "__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8081,reload=True)