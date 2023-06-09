from fastapi import APIRouter, Depends, UploadFile, status, HTTPException, File
from typing import List
from sqlalchemy.orm import Session
from data_base import oauth2, schemas, models, database
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
    "/edit/{image_name}/",
    response_model=schemas.ImageEdit,
    status_code=status.HTTP_200_OK,
)
async def get_image_data_for_edit(
    image_name: str,
    db: Session = Depends(database.get_db),
    current_user_model: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user_model.id
    return image.show_image_for_edit(image_name, db, user_id)


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
    "/{image_id}/",
    response_description="The updated image",
    status_code=status.HTTP_202_ACCEPTED,
)
def update_image(
    image_id: int,
    request: dict,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user_id = current_user.id
    return image.update(image_id, request, db, user_id)
