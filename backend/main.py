from fastapi import FastAPI, Request
from routers import image, user, authentication
from starlette.middleware.base import BaseHTTPMiddleware
import time
from data_base import models, database


app = FastAPI(title="Image-Nation_Backend", version="0.2.0")


models.Base.metadata.create_all(database.engine)


app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(image.router)


class ProccessingTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


app.add_middleware(ProccessingTimeMiddleware)


@app.get("/")
async def root():
    return {"message": "Backend is up and running!"}
