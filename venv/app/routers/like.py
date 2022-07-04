from fastapi import FastAPI, HTTPException, Response, status, Depends,APIRouter,Request
from sqlalchemy.orm import Session
from .. import models, schemas, utils,database
from . import users
router = APIRouter(
    tags=["LIKE"]
)
@router.post("/like/{id}", status_code=status.HTTP_201_CREATED)
def like(id:int,like:schemas.Like,db : Session = Depends(database.get_db),current_user: int= Depends(users.get_current_user)):

    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product with id {like.product_id} does not exist")
    like_query=db.query(models.Like).filter(models.Like.product_id == like.product_id, models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if (like.der== 1):
       if found_like:

          raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already liked product{like.product_id}")
       new_like = models.Like(product_id = like.product_id, user_id=current_user.id)
       db.add(new_like)
       db.commit()
       return{"message":"sucessfully liked"}
    else:
        if not found_like:
            
          raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already liked product{like.product_id}")

        like_query.delete(synchronize_session=False)
        db.commit()
        return{"message":"sucessfully unliked"}

