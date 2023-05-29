from fastapi import FastAPI, UploadFile, File, HTTPException, status, Request
import imageProcessing, schemas


app = FastAPI(title="Image_Processor", version="0.1.0")


@app.get("/")
def read_root():
    return {"Image_Processor": "UP!"}


@app.post("/process_image/")
async def process_image_file(image: UploadFile = File(...)) -> schemas.ImageModel:
    image_filename = image.filename
    image_data = await image.read()
    processed_image = await process_image_data_with_error_handling(
        image_data, image_filename
    )
    return processed_image.dict()


@app.get("/get_location_details")
async def get_location_details(latitude: float, longitude: float) -> schemas.Location:
    image_location_data = await get_location_details_with_error_handling(
        latitude, longitude
    )
    return image_location_data


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
    except imageProcessing.PhashCalculationError:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            f"Error calculating phash for {image_filename}",
        )
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
            return image_location_data
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


# @app.post("/phash")
# async def calculate_phash(image: UploadFile):
#     image_data = await image.read()
#     try:
#         phash_value = await imageProcessing.calculate_phash_value(image_data)
#         return {"phash_value": phash_value}
#     except imageProcessing.PhashCalculationError as e:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
#         )


# @app.post("/process_small_image")
# async def process_image(file: UploadFile):
#     image_data = await file.read()
#     try:
#         processed_image_data = await imageProcessing.process_small_image_data(
#             image_data
#         )
#         # Do something with the processed image data, e.g. return it or save it somewhere
#     except imageProcessing.SmallImageProcessingError as e:
#         raise HTTPException(
#             status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
#         )
