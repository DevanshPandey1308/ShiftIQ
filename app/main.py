from fastapi import FastAPI

from app.routers.user_router import router as user_router
from app.routers.datasets_router import router as dataset_router
from app.routers.batch_router import router as batch_router
from app.routers.ml_model_router import router as ml_model_router

app = FastAPI(
    title="ShiftIQ API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(dataset_router)
app.include_router(batch_router)
app.include_router(ml_model_router)

@app.get("/")
def home():
    return{
        "message": "Welcome to ShiftIQ API"
    }