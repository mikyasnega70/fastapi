from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..models import Todo, Users
from ..database import session_local
from typing import Annotated
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class Userverfication(BaseModel):
    current_password: str
    new_password: str=Field(min_length=6)


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    return db.query(Users).get(user.get('id'))

@router.put('/user/', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, userverify:Userverfication):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(userverify.current_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='error on password change')
    
    user_model.hashed_password = bcrypt_context.hash(userverify.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phone_number/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phonenum(user:user_dependency, db:db_dependency, phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail='authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()

