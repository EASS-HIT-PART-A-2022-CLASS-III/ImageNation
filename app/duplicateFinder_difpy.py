from typing import List
from difPy import dif
from models import SearchParams


async def find_duplicates(params: SearchParams):
    search = dif(
        params.directory,
        fast_search=params.fast_search,
        recursive=params.recursive,
        similarity=params.similarity,
        px_size=params.px_size,
        limit_extensions=params.limit_extensions,
        show_progress=params.show_progress,
        show_output=params.show_output,
        move_to=params.move_to,
        delete=params.delete,
        silent_del=params.silent_del,
        logs=params.logs
        )
    return search.result
#########
# search = dif("/mnt/c/Users/galil/test",
#               limit_extensions=True,
#               logs=True)
# print(search.lower_quality)
########

#dif(*directory, fast_search=True, recursive=True, similarity='duplicates', px_size=50, 
   # move_to=None, limit_extensions=False, show_progress=True, show_output=False, 
   # delete=False, silent_del=False, logs=False)
   ########

#    def find_duplicates(search_params: SearchParams) -> List[str]:
#     return dif(search_params.directory, **search_params.dict(exclude={'directory'})).result