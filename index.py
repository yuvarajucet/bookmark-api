from fastapi import FastAPI
import uvicorn
from routes.index import user
app = FastAPI()

app.include_router(user)

# @app.get('/')
# def read_someting():
#     return {"msg":"Hellow world"}



if __name__ == "__main__":
    uvicorn.run("index:app", host="0.0.0.0", port=8081, reload=True)