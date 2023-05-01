from typing import List
from difPy import dif
from models import SearchParams


async def find_duplicates(params: SearchParams):
    search = dif(
        params.directory
        )
    return {"results": search.result}
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