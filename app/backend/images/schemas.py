from datetime import datetime
import json
from pydantic import BaseModel, Field


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


class ImageBase(BaseModel):
    name: str = Field(..., example="image.jpg")
    content: str | None = Field(None, example="ThisIsAnImageInBase64Format")


class Image(ImageBase):
    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    email: str

    class Config:
        orm_mode = True


class ImageOut(BaseModel):
    name: str = Field(..., example="image.jpg")
    owner: UserOut

    class Config:
        orm_mode = True


class Login(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    email: str | None = None


class ImageData(BaseModel):
    smallRoundContent: str | None = Field(None)
    name: str
    country: str | None = Field(None)
    size: float | None = Field(None)
    date: datetime | None = Field(None)
    altitude: float | None = Field(None)
    direction: float | None = Field(None)
    latitude: float | None = Field(None)
    longitude: float | None = Field(None)
    phash: str | None = Field(None)


class ImagePlot(BaseModel):
    name: str
    country: str | None = Field(None)
    content: str


class ImageMap(BaseModel):
    name: str
    country: str | None = Field(None)
    direction: float | None = Field(None)
    latitude: float | None = Field(None)
    longitude: float | None = Field(None)
    smallRoundContent: str
    content: str
    date: datetime | None = Field(None)


class ImageDup(BaseModel):
    name: str
    phash: str


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


# class SearchParams(BaseModel):
#     directory: DirectoryPath | List[DirectoryPath]
#     fast_search: bool = True
#     recursive: bool = True
#     similarity: Union[str, int, float, Literal["similar"]] = "duplicates"
#     px_size: int = 50
#     limit_extensions: bool = True
#     show_progress: bool = True
#     show_output: bool = False
#     move_to: Optional[str] = None
#     delete: bool = False
#     silent_del: bool = False
#     logs: bool = False
