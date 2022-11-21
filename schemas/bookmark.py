from pydantic import BaseModel,Field

class createCategorySchema(BaseModel):
    userId:str  = Field(...)
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
    bookmarkId:str = Field(...)
    categoryName:str = Field(...)
    url:str = Field(default=None)
    label:str = Field(...)
    icon:str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxx-xxxx-xxxxx",
                "bookmarkId":"xxx-xxx-xxxx",
                "categoryName":"search engine",
                "url":"https://google.com",
                "label":"Google",
                "icon":"<Base64 encoded favicon from given URL>"
            }
        }

class editBookMarkSchema(BaseModel):
    userId:str = Field(...)
    bookmarkId:str = Field(...)
    categoryName:str = Field(...)
    url:str = Field(default=None)
    label:str = Field(...)
    icon:str = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxx-xxxx-xxxxx",
                "bookmarkId":"xxx-xxx-xxxx",
                "categoryName":"search engine",
                "url":"https://google.com",
                "label":"Google",
                "icon":"<Base64 encoded favicon from given URL>"
            }
        }

class deleteBookmarkSchema(BaseModel):
    userId:str = Field(...)
    bookmarkId:str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxxxx-xxxxx-xxxx",
                "bookmarkId":"xxxx-xxx-xxx-xxx"
            }
        }

class deleteCategorySchema(BaseModel):
    userId:str = Field(...)
    categoryId:str = Field(...)
    categoryName:str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "userId":"xxx-xxxx-xxx",
                "categoryId":"xxxx-xxx-xxxx-xxxx",
                "categoryName":"search engine"
            }
        }