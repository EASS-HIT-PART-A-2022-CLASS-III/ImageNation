from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session, joinedload
from typing import List
import models, schemas
import json
import httpx


def show_all(db: Session):
    images = db.query(models.Image).all()
    if not images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No images available"
        )
    return images


def show(id: int, db: Session):
    image = db.query(models.Image).filter(models.Image.id == id).first()
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )
    return image


def show_all_image_for_plot(db: Session, user_id: int) -> List[schemas.ImagePlot]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    images = db.query(models.Image).filter(models.Image.user_id == user_id).all()
    image_plot_list = []
    for image in images:
        image_plot = schemas.ImagePlot(
            name=image.name,
            country=image.location.country if image.location else None,
            content=image.content,
        )
        image_plot_list.append(image_plot)
    return image_plot_list


def show_all_image_for_map(db: Session, user_id: int) -> List[schemas.ImageMap]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    images = (
        db.query(models.Image)
        .options(joinedload(models.Image.gps), joinedload(models.Image.location))
        .filter(models.Image.user_id == user_id)
        .all()
    )
    image_map_list = []
    for image in images:
        image_map = schemas.ImageMap(
            name=image.name,
            country=image.location.country if image.location else None,
            direction=image.gps.direction if image.gps else None,
            latitude=image.gps.latitude if image.gps else None,
            longitude=image.gps.longitude if image.gps else None,
            smallRoundContent=image.smallRoundContent,
            content=image.content,
            date=image.date,
        )
        image_map_list.append(image_map)
    return image_map_list


def show_all_data(db: Session, user_id: int) -> List[schemas.ImageData]:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    images = (
        db.query(models.Image)
        .options(joinedload(models.Image.gps), joinedload(models.Image.location))
        .filter(models.Image.user_id == user_id)
        .all()
    )
    image_data_list = []
    for image in images:
        image_data = schemas.ImageData(
            name=image.name,
            phash=image.phash,
            size=image.size,
            date=image.date,
            altitude=image.gps.altitude if image.gps else None,
            direction=image.gps.direction if image.gps else None,
            latitude=image.gps.latitude if image.gps else None,
            longitude=image.gps.longitude if image.gps else None,
            country=image.location.country if image.location else None,
            # smallRoundContent=image.smallRoundContent,
        )
        image_data_list.append(image_data)
    return image_data_list


def create_gps(request: schemas.GPS, db: Session):
    new_gps = models.GPS(
        altitude=request.altitude if request else None,
        direction=request.direction if request else None,
        latitude=request.latitude if request else None,
        longitude=request.longitude if request else None,
    )
    db.add(new_gps)
    db.commit()
    db.refresh(new_gps)
    return new_gps


def create_location(request: schemas.Location, db: Session):
    new_location = models.Location(
        country=request.country if request else None,
        data=json.dumps(request.data) if request else None,
    )
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    return new_location


def create_image(
    request: schemas.ImageModel,
    gps: models.GPS,
    location: models.Location,
    db: Session,
    user_id: int,
):
    new_image = models.Image(
        name=request.name,
        phash=request.phash,
        size=request.size,
        date=request.date,
        content=request.content,
        smallRoundContent=request.smallRoundContent,
        user_id=user_id,
        gps_id=gps.id,
        location_id=location.id,
    )
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image


def create(request: schemas.ImageModel, db: Session, user_id: int):
    gps = create_gps(request.gps, db)
    location = create_location(request.location, db)
    image = create_image(request, gps, location, db, user_id)
    return image


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


async def process_and_create_images(
    upload_images: List[UploadFile], db: Session, current_user_id: int
):
    success_count = 0
    error_messages = []
    for upload_image in upload_images:
        image_data = await upload_image.read()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:8801/process_image/",
                    files={
                        "image": (
                            upload_image.filename,
                            image_data,
                            upload_image.content_type,
                        )
                    },
                )
            if response.status_code != 200:
                error_dict = json.loads(response.text)
                error_message = error_dict.get("detail", "Unknown error")
                error_messages.append(f"{error_message}")
                continue
            processed_image = schemas.ImageModel.parse_obj(response.json())
            create(processed_image, db, current_user_id)
            success_count += 1
        except Exception as e:
            error_messages.append(
                f"Exception for image {upload_image.filename}: {str(e)}"
            )
    return success_count, error_messages
