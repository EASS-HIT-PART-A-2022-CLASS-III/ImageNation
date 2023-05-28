from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import models, database, schemas
from hashing import Hash
from repository import user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

get_db = database.get_db


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return user.create(request, db)


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    return user.show(id, db)