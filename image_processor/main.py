from fastapi import FastAPI, UploadFile, File, HTTPException, status, Request
from typing import List
import imageProcessing, schemas


app = FastAPI(title="Image_Processor", version="0.1.0")


@app.get("/", status_code=status.HTTP_200_OK)
async def home():
    return {"message": "Image_Processor is UP"}


@app.post(
    "/process_image/", status_code=status.HTTP_200_OK, response_model=schemas.ImageModel
)
async def process_image_file(image: UploadFile = File(...)) -> schemas.ImageModel:
    image_filename = image.filename
    image_data = await image.read()
    processed_image = await process_image_data_with_error_handling(
        image_data, image_filename
    )
    return processed_image


@app.get(
    "/get_location_details/",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Location,
)
async def get_location_details(latitude: float, longitude: float) -> schemas.Location:
    image_location_data = await get_location_details_with_error_handling(
        latitude, longitude
    )
    return image_location_data


# @app.post("/find_duplicates/", status_code=status.HTTP_200_OK)
# async def find_duplicates(images: List[schemas.ImageDup]):
#     duplicates = await imageProcessing.find_duplicate_images(images)
#     return {"duplicates": duplicates}


async def process_image_data_with_error_handling(
    image_data: bytes, image_filename: str
) -> schemas.ImageModel:
    try:
        processed_image = await imageProcessing.process_image_data(
            image_data, image_filename
        )
        if processed_image is not None:
            return processed_image
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, f"Unable to process image {image_filename}"
            )
    # except imageProcessing.PhashCalculationError:
    #     raise HTTPException(
    #         status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         f"Error calculating phash for {image_filename}",
    #     )
    except imageProcessing.ErrorParsingGPSDate:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error parsing GPS and date from {image_filename}",
        )
    except imageProcessing.NoLocationDetailsFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"No location details found for {image_filename}"
        )
    except imageProcessing.ErrorGettingLocationDetails:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"Error when getting location details for {image_filename}",
        )
    except imageProcessing.SmallImageProcessingError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error when processing small image {image_filename}",
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"An error occurred processing {image_filename}: {str(e)}",
        )


async def get_location_details_with_error_handling(
    latitude: float, longitude: float
) -> schemas.Location:
    try:
        image_location_data = await imageProcessing.get_location_details(
            latitude, longitude
        )
        if image_location_data is not None:
            country = imageProcessing.get_country_name(image_location_data)
            location = schemas.Location(country=country, data=image_location_data)
            return location
        else:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                f"Unable to get location details for {latitude}, {longitude}",
            )
    except imageProcessing.NoLocationDetailsFound:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"No location details found for {latitude}, {longitude}",
        )
    except imageProcessing.ErrorGettingLocationDetails:
        raise HTTPException(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            f"Error when getting location details for {latitude}, {longitude}",
        )
    except Exception as e:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"An error occurred processing {latitude}, {longitude}: {str(e)}",
        )
