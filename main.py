from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
# from middlewares.error_handler import ErrorHandler

from routers.user import user_router
from routers.company import company_router
from routers.rig import rig_router

app = FastAPI()
app.title = "Mi aplicación"
app.version = "0.0.1"
Base.metadata.create_all(bind=engine)
# app.add_middleware(ErrorHandler)
app.include_router(user_router)
app.include_router(company_router)
app.include_router(rig_router)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello world</h1>')