from datetime import datetime
from typing import List, Optional, Union , Literal
from pydantic import BaseModel, DirectoryPath, Field

class GPS(BaseModel):
    latitude: float | None = Field(None, example=0.0)
    longitude: float | None = Field(None, example=0.0)
    altitude: float | None = Field(None, example=0.0)

class ImageModel(BaseModel):
    name: str = Field(..., example="image.jpg")
    phash: str = Field(None, example="0000000000000000")
    gps: GPS | None = Field(None)
    date: datetime | None = Field(None, example="01-01-2021 00:00:00")
    image: bytes | None = Field(None, example="bytes") 













class SearchParams(BaseModel):
    directory: DirectoryPath | List[DirectoryPath]
    fast_search: bool = True
    recursive: bool = True
    similarity: Union[str, int, float, Literal['similar']] = 'duplicates'
    px_size: int = 50
    limit_extensions: bool = True
    show_progress: bool = True
    show_output: bool = False
    move_to: Optional[str] = None
    delete: bool = False
    silent_del: bool = False
    logs: bool = False

