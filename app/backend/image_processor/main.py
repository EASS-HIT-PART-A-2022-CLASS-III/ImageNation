from fastapi import FastAPI, UploadFile, File, HTTPException, Request, status
import imageProcessing

app = FastAPI(title="Image_Processor", version="0.1.0")


@app.post("/process_image/")
async def process_image_endpoint(image: UploadFile = File(...)):
    processed_image = await imageProcessing.process_image_file(image)
    if processed_image is not None:
        return processed_image.dict()
    return {}


@app.post("/upload-image")
async def upload_image(image: UploadFile):
    try:
        address = imageProcessing.get_location_details(lat, lon)
    except imageProcessing.NoLocationDetailsFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No location details found",
        )
    except imageProcessing.ErrorGettingLocationDetails:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error when getting location details",
        )


@app.post("/upload-image")
async def upload_image(image: UploadFile):
    try:
        # processing
        lat, lon, alt, dir, date = await imageProcessing.parse_gps_and_date(image_data)
        # continue processing
    except imageProcessing.ErrorParsingGPSDate:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error when parsing GPS and date",
        )


@app.post("/phash")
async def calculate_phash(image: UploadFile):
    image_data = await image.read()
    try:
        phash_value = await imageProcessing.calculate_phash_value(image_data)
        return {"phash_value": phash_value}
    except imageProcessing.PhashCalculationError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )


@app.post("/process_small_image")
async def process_image(file: UploadFile):
    image_data = await file.read()
    try:
        processed_image_data = await imageProcessing.process_small_image_data(
            image_data
        )
        # Do something with the processed image data, e.g. return it or save it somewhere
    except imageProcessing.SmallImageProcessingError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(e)
        )
