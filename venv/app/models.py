from .database import Base
from sqlalchemy.sql.expression import text
from sqlalchemy import TIMESTAMP, Column,Integer, String , Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True , nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    image = Column(String)
    password= Column(String, nullable=False)
    is_verified = Column(Boolean , default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key= True, nullable=False)
    name =  Column(String, nullable=False)
    image = Column(String(200))
    category = Column(String(25))
    price = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner= relationship("User")


class Like(Base):
    __tablename__ = "likes"
    user_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id= Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)