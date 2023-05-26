from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
import database, schemas, oauth2, models
from repository import image

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.get(
    "/",
    response_model=List[schemas.ImageOut],
    response_description="The list of images",
    status_code=status.HTTP_200_OK,
)
def show_all(
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return image.get_all(db)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_image(
    request: schemas.Image,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return image.create(request, db)


@router.get(
    "/{id}",
    response_model=schemas.ImageOut,
    response_description="The image",
    status_code=status.HTTP_200_OK,
)
def show_image(
    id,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return image.get(id, db)


@router.delete(
    "/{id}",
    response_description="The deleted image",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_image(
    id,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return image.delete(id, db)


@router.put(
    "/{id}",
    # response_description="The updated image",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_image(
    id,
    request: schemas.Image,
    db: Session = Depends(database.get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return image.update(id, request, db)
