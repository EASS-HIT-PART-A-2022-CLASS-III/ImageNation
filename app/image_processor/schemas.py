from datetime import datetime
from pydantic import BaseModel, Field

# class ImageBase(BaseModel):
#     name: str
#     phash: str
#     size: float

# class ImageCreate(ImageBase):
#     content: bytes

# class Image(ImageBase):
#     id: Optional[int] = None
#     content: Optional[bytes] = Field(default=None)

#     class Config:
#         orm_mode = True


class Location(BaseModel):
    country: str | None = Field(None, example="Israel")
    data: dict | None = Field(None, example="city: tel aviv")


class GPS(BaseModel):
    altitude: float | None = Field(None, example=0.0)
    direction: float | None = Field(None, example=0.0)
    latitude: float | None = Field(None, example=0.0)
    longitude: float | None = Field(None, example=0.0)


class ImageModel(BaseModel):
    name: str = Field(..., example="image.jpg")
    phash: str = Field(None, example="0000000000000000")
    size: float = Field(None, example=0.0)
    gps: GPS | None = Field(None)
    location: Location | None = Field(None)
    date: datetime | None = Field(None, example="2021-01-01 00:00:00")
    content: str | None = Field(None, example="ThisIsAnImageInBase64Format")
    smallRoundContent: str | None = Field(
        None, example="ThisIsASmallRoundImageInBase64Format"
    )


class ImageDup(BaseModel):
    name: str
    phash: str
