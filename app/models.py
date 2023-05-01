from typing import List, Optional, Union , Literal
from pydantic import BaseModel, DirectoryPath
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