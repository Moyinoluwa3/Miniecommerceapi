
from fastapi import  HTTPException, Response, status, Depends,APIRouter,Request,File,UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import users
from typing import List
from .. import models, schemas, utils,database
from fastapi.staticfiles import StaticFiles
import secrets
from PIL import Image 


router = APIRouter(
    tags=['Products']
)

@router.get("/products/all", response_model=List[schemas.Product])
def get_all_products(db : Session = Depends(database.get_db), limit:int =10):
    products = db.query(models.Product, func.count(models.Like.product_id).label("likes")).join(
        models.Like, models.Like.product_id == models.Product.id, isouter=True).group_by(models.Product.id).filter().limit(limit).all()
    return products


@router.post("/products", response_model=schemas.ProductOut)
def create_new_products(product:schemas.ProductIn,db : Session = Depends(database.get_db),current_user: int= Depends(users.get_current_user)):
    new_products = models.Product(owner_id=current_user.id,**product.dict())
    db.add(new_products)
    db.commit()
    db.refresh(new_products)

    return new_products

@router.get("/products/{id}",response_model=schemas.Product)
def get_a_product(id:int,db : Session = Depends(database.get_db)):
    product = db.query(models.Product, func.count(models.Like.product_id).label("likes")).join(
        models.Like, models.Like.product_id == models.Product.id, isouter=True).group_by(models.Product.id).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user does not exist")
    return product

@router.put("/products/{id}", response_model=schemas.ProductOut)
def update_a_product(id: int,Product:schemas.ProductIn,db : Session = Depends(database.get_db),current_user: int= Depends(users.get_current_user)):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")

    product_query.update(Product.dict(), synchronize_session= False)
    db.commit()

    return product

@router.delete("/products/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db : Session= Depends(database.get_db),current_user: int= Depends(users.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id)
    if  product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= "post not found")
    

    product.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("upload/product/{id}")
async def upload_file(id:int,file:UploadFile = File(...),current_user: int= Depends(users.get_current_user),db : Session = Depends(database.get_db)):
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

    
    product = db.query(models.Products).filter(models.Product.id == id).first()
    if product.owner_id == current_user.id:
        product.image= token_name
        db.commit()
        db.refresh(product)

    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated to perform this action",
        headers={"WWW-Authenticate": "Bearer"}
    )
    file_url = "localhost:8000" + generated_name[1:]
    return{"status":"ok", "filename":file_url}






