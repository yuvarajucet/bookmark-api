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