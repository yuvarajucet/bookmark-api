from fastapi import APIRouter,Depends
from schemas.bookmark import createCategorySchema,newBookmarkSchema,editBookMarkSchema,deleteBookmarkSchema,deleteCategorySchema
from auth.athenticateUser import JWTBearer
from dbController.bookmarkDBController import *

bookmark = APIRouter(
    prefix="/api/v1/bookmark",
    tags=['bookmark'],
    responses={404:{"Description":"Not found"}}
)

@bookmark.get("/get-all-bookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def getAllBookMark():
    pass

@bookmark.post("/create-category",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def createCategory(categoryData:createCategorySchema):
    return categoryData

@bookmark.post("/add-new-bookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def addNewBookmark(bookmarkData:newBookmarkSchema):
    return bookmarkData

@bookmark.put("/edit-bookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def editBookmark(editBookmark:editBookMarkSchema):
    return editBookmark

@bookmark.delete("/delete-bookmark",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteBookmark(deleteBookmark:deleteBookmarkSchema):
    return deleteBookmark

@bookmark.delete("/deletecategory",dependencies=[Depends(JWTBearer())],tags=['bookmark'])
async def deleteCategory(deleteCategory:deleteCategorySchema):
    return deleteCategory