from fastapi import APIRouter,Depends,Body,Request,Response
from schemas.bookmark import createCategorySchema,newBookmarkSchema,editBookMarkSchema,deleteBookmarkSchema,deleteCategorySchema
from auth.athenticateUser import JWTBearer
from helper.boomarkHelper import generateCategoryId,generateBookmarId
from dbController.bookmarkDBController import createBookmarkCategory,createNewBookmark,updateBookmark,deleteBookmarkData,deleteUserCategory,getUsersAllCategory,getUsersAllBookmark

bookmark = APIRouter(
    prefix="/api/v1/bookmark",
    tags=['bookmark'],
    responses={404:{"Description":"Not found"}}
)

@bookmark.get("/getallbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def getAllBookMark(request:Request,resp:Response):
    response = getUsersAllBookmark(request)
    resp.status_code = response["status_code"]
    return response

@bookmark.post("/addnewbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def addNewBookmark(request:Request,resp:Response,bookmarkData:newBookmarkSchema):
    bookmarkData.bookmarkId = generateBookmarId()
    response = createNewBookmark(request,bookmarkData)
    resp.status_code = response["status_code"]
    return response

@bookmark.put("/editbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def editBookmark(request:Request,resp:Response,editBookmark:editBookMarkSchema):
    response = updateBookmark(request,editBookmark)
    resp.status_code = response["status_code"]
    return response

@bookmark.delete("/deletebookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteBookmarkDa(request:Request,resp:Response,deleteBookmark:deleteBookmarkSchema):
    response  = deleteBookmarkData(request,deleteBookmark)
    resp.status_code = response["status_code"]
    return response

# bookmark category routers
@bookmark.get("/getallcategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def getAllCategory(request:Request,resp:Response):
    response = getUsersAllCategory(request)
    resp.status_code = response["status_code"]
    return response

@bookmark.post("/createcategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def createCategory(request:Request,resp:Response,categoryData:createCategorySchema = Body(...)):
    categoryData.categoryId = generateCategoryId()
    response = createBookmarkCategory(request,categoryData)
    resp.status_code = response["status_code"]
    return response


@bookmark.delete("/deletecategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteCategory(request:Request,resp:Response,deleteCategory:deleteCategorySchema):
    response = deleteUserCategory(request,deleteCategory)
    resp.status_code = response["status_code"]
    return response