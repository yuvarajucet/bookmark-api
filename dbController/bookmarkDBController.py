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
        #create panrathuku munnadi category ID present ha irundha need to check user has permission for that category
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
    

def deleteBookmarkData(deleteData:deleteBookmarkSchema):
    try:
        hasOwnerShip = conn.execute("SELECT bookmarkId FROM bookmarks WHERE userid='{0}' AND bookmarkId='{1}'".format(deleteData.userId,deleteData.bookmarkId)).fetchone()
        if hasOwnerShip != None and len(hasOwnerShip):
            if deleteData.categoryId:
                conn.execute("DELETE FROM bookmarks WHERE userid='{0}' AND bookmarkId='{1}' AND categoryId='{2}'".format(deleteData.userId,deleteData.bookmarkId,deleteData.categoryId))
            else:    
                conn.execute(bookmarks.delete().where(bookmarks.c.bookmarkId == deleteData.bookmarkId))
            return createResponse(True,"Bookmark Deleted!",None)
        return createResponse(False,"Bookmark Not found or user not have permission",None)
    except Exception as e:
        return createResponse(False,"Something went wrong!",e)



def deleteUserCategory(removeCategory:deleteCategorySchema):
    try:
        hasOwnerShipOfCategory = conn.execute("SELECT userid FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId)).fetchone()
        if hasOwnerShipOfCategory != None and len(hasOwnerShipOfCategory):
            if removeCategory.removeReferedData:
                conn.execute("DELETE FROM bookmarks WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                conn.execute("DELETE FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                return createResponse(True,"Removed all the bookmark from {0}".format(removeCategory.categoryName),None)
            else:
                conn.execute("UPDATE bookmarks SET categoryId='{0}' WHERE userid='{1}' AND categoryId='{2}'".format(None,removeCategory.userId,removeCategory.categoryId))
                conn.execute("DELETE FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                return createResponse(True,"Category removed!",None)
        return createResponse(False,"category Not found!",None)
    except Exception as e:
        return createResponse(False,"Something went wrong!",e)

#------------------------------Supporting methods -------------------xxdx------

# create common response 
def createResponse(status:bool,message:str,exception:any,userData:any = None):
    return {
        "status":status,
        "message":message,
        "exception":str(exception),
        "data":userData
    }