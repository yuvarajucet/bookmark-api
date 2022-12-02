from schemas.bookmark import createCategorySchema,newBookmarkSchema,editBookMarkSchema,deleteBookmarkSchema,deleteCategorySchema
from models.model import conn,bookmarkCategory,bookmarks
from auth.authenticateHandler import decodeJWT

# create Category 
def createBookmarkCategory(request,newCategory:createCategorySchema):
    if validateUser(request,newCategory):
        try:
            conn.execute(bookmarkCategory.insert().values(
                userid = newCategory.userId,
                categoryId = newCategory.categoryId,
                categoryName = newCategory.categoryName
            ))
            return createResponse(True,"Category created",None) 
        except Exception as e:
            return createResponse(False,"Something went wrong!",e)
    return createResponse(False,"Un-authorized access",None)
    
# get all category for user:
def getUsersAllCategory(request):
    userId = getUserIdFromAuthToken(request)
    if userId != None:
        try:
            userCategory = conn.execute("SELECT categoryName,categoryId FROM BMCategory WHERE userid='{0}'".format(userId)).fetchall()
            jsonObject = generateCategoryJsonObject(userCategory,userId)
            return createResponse(True,"Fetched..",None,jsonObject)
        except Exception as e:
            return createResponse(False,"Something went worng!",e)
    return createResponse(False,"Authorization failed!",None)
    
# add new bookmark
def createNewBookmark(request,bookmarkData:newBookmarkSchema):
    if validateUser(request,bookmarkData):
        try:
            isValidCategoryId = False
            if bookmarkData.categoryId != 'default':
                categoryId = conn.execute("SELECT categoryId FROM BMCategory WHERE categoryId='{0}' AND userid='{1}'".format(bookmarkData.categoryId,bookmarkData.userId)).fetchone()
                if categoryId != None and len(categoryId):
                    isValidCategoryId = True
            if bookmarkData.categoryId == 'default' or isValidCategoryId:
                conn.execute(bookmarks.insert().values(
                    userid = bookmarkData.userId,
                    bookmarkId = bookmarkData.bookmarkId,
                    categoryId = bookmarkData.categoryId,
                    url = bookmarkData.url,
                    label = bookmarkData.label,
                    icon = bookmarkData.icon
                ))
                return createResponse(True,"Bookmark succssfully added!",None)
            return createResponse(False,"Invalid CategoryId",None)
        except Exception as e :
            return createResponse(False,"Something went wrong!",e)
    return createResponse(False,"Un-authorized access",None)

# get all bookmarks for user:
def getUsersAllBookmark(request):
    userId = getUserIdFromAuthToken(request)
    if userId != None:
        try:
            userCategory = conn.execute("SELECT categoryId FROM bookmarks WHERE userid='{0}' GROUP BY categoryId".format(userId)).fetchall()
            userDataObject = beautifyUserBookmarkData(userCategory,userId)
            return createResponse(True,"user data fetched!",None,userDataObject)
        except Exception as e:
            return createResponse(False,"Something went wrong!",e)
    return createResponse(False,"Authorization failed!",None)

# update bookmark (Edit bookmark)
def updateBookmark(request,editedData:editBookMarkSchema):
    if validateUser(request,editedData):
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
    return createResponse(False,"Un-authorized access",None)
    
# remove or delete bookmark
def deleteBookmarkData(request,deleteData:deleteBookmarkSchema):
    if validateUser(request,deleteData):
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
    return createResponse(False,"Un-authorized access",None)

# remove or delete category
def deleteUserCategory(request,removeCategory:deleteCategorySchema):
    if validateUser(request,removeCategory):
        try:
            hasOwnerShipOfCategory = conn.execute("SELECT userid FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId)).fetchone()
            if hasOwnerShipOfCategory != None and len(hasOwnerShipOfCategory):
                if removeCategory.removeReferedData:
                    conn.execute("DELETE FROM bookmarks WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                    conn.execute("DELETE FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                    return createResponse(True,"Removed all the bookmark from {0}".format(removeCategory.categoryName),None)
                else:
                    conn.execute("UPDATE bookmarks SET categoryId='{0}' WHERE userid='{1}' AND categoryId='{2}'".format("default",removeCategory.userId,removeCategory.categoryId))
                    conn.execute("DELETE FROM BMCategory WHERE userid='{0}' AND categoryId='{1}'".format(removeCategory.userId,removeCategory.categoryId))
                    return createResponse(True,"Category removed!",None)
            return createResponse(False,"category Not found!",None)
        except Exception as e:
            return createResponse(False,"Something went wrong!",e)
    return createResponse(False,"Un-authorized access",None)




#------------------------------Supporting methods -------------------------
    
# get userID via JWT token
def getUserIdFromAuthToken(request):
    headers = request.headers
    if "Authorization" in headers:
        authToken = headers["Authorization"]
        splitToken = authToken.split(' ')
        if len(splitToken) > 1:
            decodedAuthToken = decodeJWT(splitToken[1])
            if decodedAuthToken != None:
                return decodedAuthToken["userId"]
    return None

# make json object for user category:
def generateCategoryJsonObject(datas,userId):
    categoryObject = []
    for categoryName,categoryId in datas:
        category = {"category_name":categoryName,"category_id":categoryId}
        categoryObject.append(category)
    return {
        "userId":userId,
        "userData":categoryObject
    }

# make user data structre and fill data
def beautifyUserBookmarkData(userCategory,userid):
    data = {
            "userId":userid,
            "userData":getUserDataFromCategoryId(userCategory,userid)
        }
    return data

# make category structue and fill data
def getUserDataFromCategoryId(userCategory,userId):
    data = []
    for category in userCategory:
        categoryId = category[0]
        data.append(
            {
                "categoryId":categoryId,
                "categoryName" : getCategoryNameWithId(categoryId),
                "bookmarks": getBookmarkWithCategoryId(categoryId,userId)
            }
        )
    return data

# get category name using category ID
def getCategoryNameWithId(categoryId):
    if categoryId != None:
        try:
            categroyName = conn.execute("SELECT categoryName FROM BMCategory WHERE categoryId='{0}'".format(categoryId)).fetchone()
            if len(categroyName):
                return categroyName[0]
            return None
        except:
            return None
    return None

# fetch all bookmark data which contain that category ID
def getBookmarkWithCategoryId(categoryId,userId):
    try:
        bookmarkData = conn.execute("SELECT bookmarkId,url,label,icon FROM bookmarks WHERE categoryId='{0}' AND userid='{1}'".format(categoryId,userId)).fetchall()
        if bookmarkData != None and len(bookmarkData):
            return beatifyBookmarkData(bookmarkData)
    except Exception as e :
        return None


# construct bookmark object with given data
def beatifyBookmarkData(bookmarkData):
    data = []
    for bookmarkId,url,label,icon in bookmarkData:
        data.append(
            {
                "bookmarkId":bookmarkId,
                "url":url,
                "label":label,
                "icon":icon
            }
        )
    return data

# validate userId with Auth token
def validateUser(request,data)->bool:
    userId = getUserIdFromAuthToken(request)
    if userId != None:
        if userId == data.userId:
            return True
    return False

# create common response 
def createResponse(status:bool,message:str,exception:any,userData:any = None):
    return {
        "status":status,
        "message":message,
        "exception":str(exception),
        "data":userData
    }