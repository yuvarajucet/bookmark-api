from fastapi import APIRouter
from dbController.adminDBController import createTables

admin = APIRouter(
    prefix='/api/v1/admin',
    tags=['admin'],
    responses={404:{"Description":"Not found"}}
)

@admin.get("/createdb",tags=['admin'])
async def index():
    resp = createTables()
    return resp

@admin.get("/exportall",tags=['admin'])
async def exprtall():
    return {
        "message":"Not implemented"
    }

@admin.post("/importall",tags=['admin'])
async def importall():
    return{
        "message":"Not implemented"
    }