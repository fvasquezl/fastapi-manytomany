from fastapi import FastAPI
from app.config.database import engine
from app.middleware.db_session import DBSessionMiddleware
from app.config.database import engine, Base
from app.routers.password_routers import password_router
from app.routers.tag_routers import tag_router
from app.routers.category_routers import category_router
from app.routers.user_routers import user_router


app = FastAPI()
app.add_middleware(DBSessionMiddleware)
app.include_router(password_router)
app.include_router(tag_router)
app.include_router(category_router)
app.include_router(user_router)


Base.metadata.create_all(bind=engine)
