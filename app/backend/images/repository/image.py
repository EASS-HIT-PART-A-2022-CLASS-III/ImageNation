from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas


def get_all(db: Session):
    images = db.query(models.Image).all()
    if not images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No images available"
        )
    return images


def get(id: int, db: Session):
    image = db.query(models.Image).filter(models.Image.id == id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )
    return image


def create(request: schemas.Image, db: Session):
    new_image = models.Image(name=request.name, content=request.content, user_id=1)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def delete(id: int, db: Session):
    image = db.query(models.Image).filter(models.Image.id == id)
    if not image.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )
    image.delete(synchronize_session=False)
    db.commit()
    return {"message": f"image with the id: {id} deleted"}


def update(id: int, request: schemas.Image, db: Session):
    image = db.query(models.Image).filter(models.Image.id == id)
    if not image.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} not found",
        )
    image.update(request.dict())
    db.commit()
    return {"message": f"image with the id: {id} updated"}
