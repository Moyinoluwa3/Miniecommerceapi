from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import users,like,products
import time
from . import utils


#image upload
from fastapi import File, UploadFile
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image 




models.Base.metadata.create_all(bind=engine)

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)

#app.mount("/static", StaticFiles(directory="./app/static"),name="static")






while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi',user='postgres', password='moyin',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connection was sucessful')
        break
    except Exception as error:
        print('database connection was not sucessful!!')
        print('error:', error)
        time.sleep(2)


app.include_router(users.router)
app.include_router(utils.router)
app.include_router(like.router)
app.include_router(products.router)
