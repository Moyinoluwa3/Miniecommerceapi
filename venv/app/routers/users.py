from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter,Request,File,UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi_mail import FastMail
from itsdangerous import URLSafeTimedSerializer  as Serializer
import datetime
from fastapi.security.oauth2 import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from ..utils import send_mail as sendmail

from typing import List
from . import auth
auth_handler = auth.Auth()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
from .. import models, schemas, utils
from .auth import Auth
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image 


from ..database import get_db
#app.mount("/static", StaticFiles(directory="static"),name="static")
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

auth_handler = Auth()

@router.get("/",response_model=List[schemas.UserOutput])
def get_all_users(db : Session = Depends(get_db) ):
    users = db.query(models.User).all()
    return users




@router.post("/", status_code=201, response_model=schemas.UserOutput )
def sign_up(user: schemas.UserCreate,db : Session = Depends(get_db)):
    email =  db.query(models.User).filter(models.User.email == user.email).first()
    email = jsonable_encoder(email)
    print(email)
    if  email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= "User exists")
    try:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user= models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as err:
        return {"message" : err}


@router.post('/login', response_model=schemas.Token)

def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    print (user)
    
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"invalid credentials")
   
    access_token = auth_handler.encode_token(user.id)

    return {"access_token": access_token, "token_type": "bearer"}





@router.get('/{id}',response_model=schemas.UserOutput)
def Get_user(id: int,db : Session = Depends(get_db) ):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")

    return user

            


def get_current_user(token: str = Depends(oauth2_scheme),db : Session = Depends(get_db) ):

    token_data = auth_handler.decode_token(token)
   
    user = db.query(models.User).filter(models.User.id == token_data).first()
    return user

@router.post("upload/profile/{id}")
async def upload_file(id:int,file:UploadFile = File(...),current_user: int= Depends(get_current_user),db : Session = Depends(get_db)):
    FILEPATH = "./static/images/"
    filename = file.filename
    extension = filename.split(".")[1]
    if extension not in ["png","jpg"]:
        return {"status":"error", "detail":"file not supported"}

    token_name = secrets.token_hex(10)+"."+extension
    generated_name = FILEPATH + token_name
    file_content =  await file.read()

    with open(generated_name, "wb") as file:
        file.write(file_content)

    

#pillow
    img = Image.open(generated_name)
    img = img.resize(size=(200,200))
    img.save(generated_name)
    file.close()

    user = db.query(models.User).filter(models.User.id == id).first()
    if user == current_user:
        user.image= token_name
        db.commit()
        db.refresh(user)

    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated to perform this action",
        headers={"WWW-Authenticate": "Bearer"}
    )
    file_url = "localhost:8000" + generated_name[1:]
    return{"status":"ok", "filename":file_url}


