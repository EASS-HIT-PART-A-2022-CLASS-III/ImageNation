from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
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
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.show_all(db, user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_image(
    upload_images: List[UploadFile] = File(...),
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    current_user = schemas.UserBase.from_orm(current_user_model)
    (
        success_count,
        error_messages,
        uploaded_images,
    ) = await image.process_and_create_images(upload_images, db, current_user.id)
    return {
        "success": success_count,
        "errors": error_messages,
        "uploaded_images": uploaded_images,
    }


@router.get(
    "/data/", response_model=List[schemas.ImageData], status_code=status.HTTP_200_OK
)
async def get_user_images_df(
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return image.show_all_data(db, user_id)


@router.get(
    "/plot/", response_model=List[schemas.ImagePlot], status_code=status.HTTP_200_OK
)
async def get_user_images_plot(
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return image.show_all_image_for_plot(db, user_id)


@router.get("/names/", response_model=List[str], status_code=status.HTTP_200_OK)
async def get_image_names(
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return image.show_all_image_names(db, user_id)


@router.get(
    "/map/", response_model=List[schemas.ImageMap], status_code=status.HTTP_200_OK
)
async def get_user_images_map(
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return image.show_all_image_for_map(db, user_id)


@router.get(
    "/find_duplicates/",
    response_description="The duplicate images",
    status_code=status.HTTP_200_OK,
)
async def find_duplicate(
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return await image.show_all_duplicates(db, user_id)


@router.get(
    "/{id}",
    response_model=schemas.ImageOut,
    response_description="The image",
    status_code=status.HTTP_200_OK,
)
def show_image(
    id,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.show(id, db, user_id)


@router.delete(
    "/id/{id}/",
    response_description="The deleted image",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_image(
    id,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.delete_by_id(id, db, user_id)


@router.delete(
    "/name/{image_name}/",
    response_description="The deleted image",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_image_by_name(
    image_name: str,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.delete_by_name(image_name, db, user_id)


@router.put(
    "/{id}",
    # response_description="The updated image",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_image(
    id,
    request: schemas.Image,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.update(id, request, db, user_id)


# @router.put("/update_image_gps/{image_id}")
# async def update_image_gps_endpoint(image_id: int, latitude: float, longitude: float):
#     # Retrieve the image details from the database using the image_id
#     image = session.query(ImageModel).get(image_id)
#     if image is None:
#         raise HTTPException(status_code=404, detail="Image not found")

#     # Update the GPS coordinates in the image details
#     image.gps = GPS(latitude=latitude, longitude=longitude)

#     # Update the location details based on the new coordinates
#     async with httpx.AsyncClient() as client:
#         response = await client.get(f"http://location_service:8000/get_location_details?latitude={latitude}&longitude={longitude}")
#         location_data = response.json()

#     image.location = Location(country=location_data['country'], data=location_data)

#     # Save the updated image details back to the database
#     session.commit()

#     return {"message": f"Image {image_id} GPS coordinates updated successfully."}
# @app.get(
#     "/images",
#     response_model=List[schemas.ImageOut],
#     response_description="The list of images",
#     status_code=status.HTTP_200_OK,
# )
# def show_all(db: Session = Depends(get_db)):
#     images = db.query(models.Image).all()
#     if not images:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No images available")
#     return images


# @app.get(
#     "/images/{image_name}/imageLocationData",
#     response_description="The location data of the image",
#     status_code=status.HTTP_200_OK,
# )
# async def get_image_location_data(image_name: str):
#     if image_name not in database:
#         raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
#     image_obj = database[image_name]
#     location_data = image_obj.location
#     if location_data:
#         return {"locatin_data": location_data}
#     else:
#         return {"message": "Location data is not available for this image."}


# @app.get("/", status_code=status.HTTP_200_OK)
# async def home():
#     return {"message": "IMAGE-NATION is UP"}


# @app.post(
#     "/images/",
#     response_description="The created images",
#     status_code=status.HTTP_201_CREATED,
# )
# async def upload_and_calculate_phash(images: List[UploadFile] = File(...)):
#     for image in images:
#         image_obj = await process_image_file(image)
#         if image_obj:
#             database[image_obj.name] = image_obj
#     return {"status": "success", "message": f"{len(images)} images uploaded"}


# @app.get(
#     "/images/{image_name}/get_image_gps_data",
#     response_description="Get GPS data of the image",
#     status_code=status.HTTP_200_OK,
# )
# async def get_image_gps_data(image_name: str):
#     if image_name not in database:
#         raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
#     image_obj = database[image_name]
#     gps_data = image_obj.gps
#     if gps_data:
#         return {"gps_data": gps_data}
#     else:
#         return {"message": "GPS data is not available for this image."}


# @app.patch(
#     "/patchImage/{image_name}",
#     response_description="The updated image",
#     status_code=status.HTTP_202_ACCEPTED,
# )
# async def patch_image(image_name: str, image: ImageModel):
#     if image_name not in database:
#         raise HTTPException(status_code=404, detail=f"Image {image_name} not found")
#     stored_image_data = database.get(image_name)
#     if stored_image_data is not None:
#         update_data = image.dict(exclude_unset=True)
#         for field, value in update_data.items():
#             if value is not None:
#                 setattr(stored_image_data, field, value)
#         database[image_name] = stored_image_data
#         return {"image": stored_image_data.dict()}
#     else:
#         database[image_name] = image.dict()
#         return {"status": "success", "message": f"{image_name} updated"}
