from datetime import datetime
import json
from pydantic import BaseModel, Field, DirectoryPath


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

class Image(BaseModel):
    name: str = Field(..., example="image.jpg")
    content: str | None = Field(None, example="ThisIsAnImageInBase64Format")
    

class ShowImage(BaseModel):
    name: str = Field(..., example="image.jpg")
    class Config():
        orm_mode = True

class User(BaseModel):
    name: str
    email: str
    password: str
    class Config():
        orm_mode = True

class UserOut(BaseModel):
    name: str
    email: str
    class Config():
        orm_mode = True


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)