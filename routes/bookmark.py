from fastapi import APIRouter,Depends,Body
from schemas.bookmark import createCategorySchema,newBookmarkSchema,editBookMarkSchema,deleteBookmarkSchema,deleteCategorySchema
from auth.athenticateUser import JWTBearer
from helper.boomarkHelper import generateCategoryId,generateBookmarId
from dbController.bookmarkDBController import createBookmarkCategory,createNewBookmark,updateBookmark

bookmark = APIRouter(
    prefix="/api/v1/bookmark",
    tags=['bookmark'],
    responses={404:{"Description":"Not found"}}
)

@bookmark.get("/getallbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def getAllBookMark():
    pass

@bookmark.post("/addnewbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def addNewBookmark(bookmarkData:newBookmarkSchema):
    bookmarkData.bookmarkId = generateBookmarId()
    response = createNewBookmark(bookmarkData)
    return response

@bookmark.put("/editbookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def editBookmark(editBookmark:editBookMarkSchema):
    response = updateBookmark(editBookmark)
    return response

@bookmark.delete("/deletebookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteBookmark(deleteBookmark:deleteBookmarkSchema):
    return deleteBookmark


# bookmark category routers
@bookmark.get("/getallcategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def getAllCategory():
    pass

@bookmark.post("/createcategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def createCategory(categoryData:createCategorySchema = Body(...)):
    categoryData.categoryId = generateCategoryId()
    response = createBookmarkCategory(categoryData)
    return response


@bookmark.delete("/deletecategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteCategory(deleteCategory:deleteCategorySchema):
    return deleteCategory