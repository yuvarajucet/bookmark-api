from schemas.bookmark import createCategorySchema,newBookmarkSchema,editBookMarkSchema,deleteBookmarkSchema,deleteCategorySchema
from models.model import conn,bookmarkCategory,bookmarks

# create Category 
def createBookmarkCategory(newCategory:createCategorySchema):
    try:
        conn.execute(bookmarkCategory.insert().values(
            userid = newCategory.userId,
            categoryId = newCategory.categoryId,
            categoryName = newCategory.categoryName
        ))
        return createResponse(True,"Category created",None) 
    except Exception as e:
        return createResponse(False,"Something went wrong!",e)

    
# add new bookmark
def createNewBookmark(bookmarkData:newBookmarkSchema):
    try:
        conn.execute(bookmarks.insert().values(
            userid = bookmarkData.userId,
            bookmarkId = bookmarkData.bookmarkId,
            categoryId = bookmarkData.categoryId,
            url = bookmarkData.url,
            label = bookmarkData.label,
            icon = bookmarkData.icon
        ))
        return createResponse(True,"Bookmark succssfully added!",None)
    except Exception as e :
        return createResponse(False,"Something went wrong!",e)
    


def updateBookmark(editedData:editBookMarkSchema):
    try:
        #check user's ownership of category and bookmark
        isValidCategoryId = conn.execute("SELECT userid FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(editedData.userId,editedData.categoryId)).fetchone()
        if isValidCategoryId !=None and len(isValidCategoryId):
            hasOwnerShip = conn.execute("SELECT bookmarkId FROM bookmarks WHERE userid='{0}' AND bookmarkId='{1}'".format(editedData.userId,editedData.bookmarkId)).fetchone()
            if hasOwnerShip != None and len(hasOwnerShip):
                conn.execute(bookmarks.update().values(
                    categoryId = editedData.categoryId,
                    url = editedData.url,
                    label = editedData.label,
                    icon = editedData.icon
                ).where(bookmarks.c.bookmarkId == editedData.bookmarkId))
                return createResponse(True,"Bookmark Edited!",None)
            return createResponse(False,"User not have access to this bookmark!",None)
        return createResponse(False,"User doesn't have this Category",None)
    except Exception as e:
        return createResponse(False,"Something went wrong!",e)
    
#------------------------------Supporting methods -------------------------

# create common response 
def createResponse(status:bool,message:str,exception:any,userData:any = None):
    return {
        "status":status,
        "message":message,
        "exception":str(exception),
        "data":userData
    }