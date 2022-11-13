from fastapi import APIRouter

bookmark = APIRouter(
    prefix="/api/v1/bookmark",
    tags=['bookmark'],
    responses={404:{"Description":"Not found"}}
)

@bookmark.get("/get-all-bookmark",tags=['bookmark'])
def getAllBookMark():
    pass

@bookmark.post("/add-new-bookmark",tags=['bookmark'])
def addNewBookmark():
    pass

@bookmark.put("/edit-bookmark",tags=['bookmark'])
def editBookmark():
    pass

@bookmark.delete("/delete-bookmark",tags=['bookmark'])
def deleteBookmark():
    pass