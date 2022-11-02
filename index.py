from fastapi import FastAPI
from routes.index import user
app = FastAPI()

app.include_router(user)

# @app.get('/')
# def read_someting():
#     return {"msg":"Hellow world"}