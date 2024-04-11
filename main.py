from fastapi import FastAPI

# from app.middleware.db_session import DBSessionMiddleware

from app.routers.password_routers import router as password_router

# from app.routers.tag_routers import tag_router
# from app.routers.category_routers import category_router
from app.routers.user_routers import router as user_router


app = FastAPI()
# app.add_middleware(DBSessionMiddleware)
app.include_router(password_router)
# app.include_router(tag_router)
# app.include_router(category_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return "Server is running."
