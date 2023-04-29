from fastapi import FastAPI
from models import SearchParams
from duplicateFinder_difpy import find_duplicates
from typing import List, Optional, Union , Literal
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "JUST A TEST"}

@app.post("/run_search")
async def run_search(params: SearchParams):
    results = find_duplicates(params)
    return {"results": results}