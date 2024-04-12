from fastapi import FastAPI

# from app.middleware.db_session import DBSessionMiddleware

from app.routers.post_routers import router as post_router
from app.routers.tag_routers import router as tag_router
from app.routers.category_routers import router as category_router
from app.routers.user_routers import router as user_router
from app.routers.role_routers import router as role_router

description = """
PwdMgmt API helps you do awesome stuff. 🚀

## Users

You can **read items**.

## Posts

You will be able to:

* **Create users**.
* **Read users**.
* **Create Posts**.
"""

tags_metadata = [
    {
        "name": "Users",
        "description": "Operations with users. The **login** logic is also here.",
    },{
        "name": "Roles",
        "description": "Manage Roles. So _fancy_ they have their own docs.",
    },{
        "name": "Posts",
        "description": "Manage posts. So _fancy_ they have their own docs.",
    },{
        "name": "Tags",
        "description": "Manage Tags. So _fancy_ they have their own docs.",
    },{
        "name": "Categories",
        "description": "Manage Tags. So _fancy_ they have their own docs.",
    },{
        "name": "Root",
        "description": "Root",
    },
]



app = FastAPI(
    title="PwdMgmt",
    description=description,
    summary="App to manage personal posts.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Faustino Vasquez",
        "url": "http://galaxy.example.com/contact/",
        "email": "adm@galaxy-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },openapi_tags=tags_metadata)

# app.add_middleware(DBSessionMiddleware)
app.include_router(post_router, tags=["Posts"])
app.include_router(tag_router, tags=["Tags"])
app.include_router(category_router, tags=["Categories"])
app.include_router(user_router, tags=["Users"])
app.include_router(role_router, tags=["Roles"])


@app.get("/",tags=['Root'])
def read_root():
    return "Server is running."
