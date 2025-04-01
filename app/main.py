from fastapi import FastAPI, Request 
from app import models, database
from app.routers import data, query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# # Custom handler for 422 errors
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request: Request, exc: RequestValidationError):
#     for error in exc.errors():
#         if error["type"] == "type_error.float":
#             return JSONResponse(
#                 status_code=422,
#                 content=jsonable_encoder({
#                     "detail": "Temperature, humidity, and windspeed must be numeric values (float)."
#                 }),
#             )
#     # fallback to show original FastAPI validation errors
#     return JSONResponse(
#         status_code=422,
#         content=jsonable_encoder({"detail": exc.errors()}),
#     )

# Include router
app.include_router(data.router)
app.include_router(query.router)

# define basic GET endpoint 
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Weather Sensor API!",
        "docs": "Visit http://127.0.0.1:8000/docs to enter sensor data via interactive docs"
    }
