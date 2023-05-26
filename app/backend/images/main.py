from fastapi import FastAPI
import models
from database import engine
from routers import image, user, authentication


app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(image.router)


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
