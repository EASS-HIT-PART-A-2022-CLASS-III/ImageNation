from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from data_base import models, schemas
import json
import httpx
from datetime import datetime

API_URL = "http://image_processor:8801"


def show_all(db: Session, user_id: int) -> List[schemas.Image]:
    images = db.query(models.Image).filter(models.Image.user_id == user_id).all()
    if not images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No images available"
        )
    return images


def show(id: int, db: Session, user_id: int) -> schemas.Image:
    image = (
        db.query(models.Image)
        .filter(models.Image.user_id == user_id)
        .filter(models.Image.id == id)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )
    return image


def show_all_image_for_plot(db: Session, user_id: int) -> List[schemas.ImagePlot]:
    images = (
        db.query(models.Image)
        .options(joinedload(models.Image.location))
        .filter(models.Image.user_id == user_id)
        .all()
    )
    if not images:
        raise HTTPException(status_code=404, detail="No images found for user")
    image_plot_list = []
    for image in images:
        image_plot = schemas.ImagePlot(
            name=image.name,
            country=image.location.country if image.location else "Unknown",
            content=image.content,
        )
        image_plot_list.append(image_plot)
    return image_plot_list


def show_image_for_edit(
    image_name: str, db: Session, user_id: int
) -> schemas.ImageEdit:
    image = (
        db.query(models.Image)
        .options(joinedload(models.Image.gps))
        .filter(models.Image.user_id == user_id)
        .filter(models.Image.name == image_name)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )

    image_edit = schemas.ImageEdit(
        id=image.id,
        name=image.name,
        content=image.content,
        date=image.date,
        altitude=image.gps.altitude if image.gps else 0,
        direction=image.gps.direction if image.gps else 0,
        latitude=image.gps.latitude if image.gps else 0,
        longitude=image.gps.longitude if image.gps else 0,
    )
    return image_edit


def show_all_image_for_map(db: Session, user_id: int) -> List[schemas.ImageMap]:
    images = (
        db.query(models.Image)
        .options(joinedload(models.Image.gps), joinedload(models.Image.location))
        .filter(models.Image.user_id == user_id)
        .all()
    )
    if not images:
        raise HTTPException(status_code=404, detail="No images found for user")
    image_map_list = []
    for image in images:
        image_map = schemas.ImageMap(
            name=image.name,
            country=image.location.country if image.location else "Unknown",
            direction=image.gps.direction if image.gps else 0,
            latitude=image.gps.latitude if image.gps else 0,
            longitude=image.gps.longitude if image.gps else 0,
            smallRoundContent=image.smallRoundContent,
            content=image.content,
            date=image.date,
        )
        image_map_list.append(image_map)
    return image_map_list


def show_all_image_names(db: Session, user_id: int) -> List[str]:
    image_names = (
        db.query(models.Image.name).filter(models.Image.user_id == user_id).all()
    )
    image_names = [name[0] for name in image_names]
    return image_names


def show_all_data(db: Session, user_id: int) -> List[schemas.ImageData]:
    images = (
        db.query(models.Image)
        .options(joinedload(models.Image.gps), joinedload(models.Image.location))
        .filter(models.Image.user_id == user_id)
        .all()
    )

    if not images:
        raise HTTPException(status_code=404, detail="No images found for user")
    image_data_list = []
    for image in images:
        image_data = schemas.ImageData(
            smallRoundContent=image.smallRoundContent,
            name=image.name,
            size=image.size,
            date=image.date,
            altitude=image.gps.altitude if image.gps else 0,
            direction=image.gps.direction if image.gps else 0,
            latitude=image.gps.latitude if image.gps else 0,
            longitude=image.gps.longitude if image.gps else 0,
            country=image.location.country if image.location else "Unknown",
            phash=image.phash,
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


def delete_by_id(id: int, db: Session, user_id: int):
    image = (
        db.query(models.Image)
        .filter(models.Image.user_id == user_id)
        .filter(models.Image.id == id)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {id} is not available",
        )
    db.delete(image)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the image.",
        )
    return {"message": f"image with the id: {id} deleted"}


def delete_by_name(name: str, db: Session, user_id: int):
    image = (
        db.query(models.Image)
        .filter(models.Image.user_id == user_id)
        .filter(models.Image.name == name)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the name {name} is not available",
        )
    db.delete(image)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the image.",
        )
    return {"message": f"image with the name: {name} deleted"}


from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime


def update(image_id: str, request: dict, db: Session, user_id: int):
    image = (
        db.query(models.Image)
        .filter(models.Image.user_id == user_id)
        .filter(models.Image.id == image_id)
        .first()
    )
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Image with the id {image_id} not found",
        )
    for attr, value in request.items():
        if value is None:
            continue  # Skip None values
        if attr in ["gps", "location"] and isinstance(value, dict):
            attr_obj = getattr(image, attr, None)
            if attr_obj is not None:
                for field, field_value in value.items():
                    setattr(attr_obj, field, field_value)
                setattr(image, attr, attr_obj)
        elif attr == "date":
            date_object = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            setattr(image, attr, date_object)
        else:
            setattr(image, attr, value)
    db.commit()
    return {"message": f"image with the id: {image_id} updated"}


async def show_all_duplicates(db: Session, user_id: int):
    images = db.query(models.Image).filter(models.Image.user_id == user_id).all()
    if not images:
        raise HTTPException(status_code=404, detail="No images found for user")
    image_dups = []
    for image in images:
        image_dup = schemas.ImageDup(name=image.name, phash=image.phash)
        image_dups.append(image_dup.dict())
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{API_URL}/find_duplicates/",
                json=image_dups,
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No duplicates found"
            )
        return response.json()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unavailable",
        )


async def process_and_create_images(
    upload_images: List[UploadFile], db: Session, current_user_id: int
):
    success_count = 0
    error_messages = []
    uploaded_images = []
    for upload_image in upload_images:
        image_data = await upload_image.read()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/process_image/",
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
            existing_image = (
                db.query(models.Image)
                .filter(models.Image.user_id == current_user_id)
                .filter(models.Image.name == processed_image.name)
                .first()
            )
            if existing_image:
                error_messages.append(
                    f"Exception for image {upload_image.filename}: Image with the same name already exists."
                )
                continue
            create(processed_image, db, current_user_id)
            success_count += 1
            uploaded_images.append(processed_image.name)
        except Exception as e:
            error_messages.append(
                f"Exception for image {upload_image.filename}: {str(e)}"
            )
    return success_count, error_messages, uploaded_images
