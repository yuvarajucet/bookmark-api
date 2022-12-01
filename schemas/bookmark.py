from pydantic import BaseModel,Field

class createCategorySchema(BaseModel):
    userId:str  = Field(...)
    categoryId:str = Field(default=None)
    categoryName:str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxx-xxxx-xxxx-xxx",
                "categoryName":"search engine"
            }
        }

class newBookmarkSchema(BaseModel):
    userId:str = Field(...)
    bookmarkId:str = Field(default=None)
    categoryId:str = Field(default="default")
    url:str = Field(default=None)
    label:str = Field(...)
    icon:str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxx-xxxx-xxxxx",
                "categoryId":"xxx-xxx-xxx(Optional)",
                "url":"https://google.com",
                "label":"Google"
            }
        }

class editBookMarkSchema(BaseModel):
    userId:str = Field(...)
    bookmarkId:str = Field(...)
    categoryId:str = Field(...)
    url:str = Field(default=None)
    label:str = Field(...)
    icon:str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxx-xxxx-xxxxx",
                "bookmarkId":"xxx-xxx-xxxx",
                "categoryId":"xxxx-xxxx-xxxx",
                "url":"https://google.com",
                "label":"Google"
            }
        }

class deleteBookmarkSchema(BaseModel):
    userId:str = Field(...)
    bookmarkId:str = Field(...)
    categoryId:str = Field(default=None)
    url:str = Field(default=None)
    label:str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxxx-xxxxx-xxxx",
                "bookmarkId":"xxxx-xxx-xxx-xxx",
                "categoryId":"xx-xxx-xxx-xxx",
                "url":"https://example.com",
                "label":"example"
            }
        }

class deleteCategorySchema(BaseModel):
    userId:str = Field(...)
    categoryId:str = Field(...)
    categoryName:str = Field(default=None)
    removeReferedData:bool = Field(default=False)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxx-xxxx-xxx",
                "categoryId":"xxxx-xxx-xxxx-xxxx",
                "categoryName":"search engine",
                "removeReferedData": False
            }
        }