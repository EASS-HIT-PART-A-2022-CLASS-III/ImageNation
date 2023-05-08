from datetime import datetime
import json
from typing import List, Optional, Union, Literal
from pydantic import BaseModel, DirectoryPath, Field


class GPS(BaseModel):
    latitude: float | None = Field(None, example=0.0)
    longitude: float | None = Field(None, example=0.0)
    altitude: float | None = Field(None, example=0.0)


class ImageModel(BaseModel):
    name: str = Field(..., example="image.jpg")
    phash: str = Field(None, example="0000000000000000")
    gps: GPS | None = Field(None)
    date: datetime | None = Field(None, example="2021-01-01 00:00:00")
    content: str | None = Field(None, example="kjhfdfasf")


class DateTimeEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, datetime):
            return str(z)
        else:
            return super().default(z)


class SearchParams(BaseModel):
    directory: DirectoryPath | List[DirectoryPath]
    fast_search: bool = True
    recursive: bool = True
    similarity: Union[str, int, float, Literal["similar"]] = "duplicates"
    px_size: int = 50
    limit_extensions: bool = True
    show_progress: bool = True
    show_output: bool = False
    move_to: Optional[str] = None
    delete: bool = False
    silent_del: bool = False
    logs: bool = False
