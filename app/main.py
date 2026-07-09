from fastapi import FastAPI

from app.routers.user_router import router as user_router
from app.routers.datasets_router import router as dataset_router
from app.routers.batch_router import router as batch_router
from app.routers.ml_model_router import router as ml_model_router

from app.routers.drift_report_router import router as drift_report_router

from app.routers.alert_router import router as alert_router

from app.routers.ai_insight_router import router as ai_insight_router

app = FastAPI(
    title="ShiftIQ API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(dataset_router)
app.include_router(batch_router)
app.include_router(ml_model_router)
app.include_router(drift_report_router)
app.include_router(alert_router)
app.include_router(ai_insight_router)

@app.get("/")
def home():
    return{
        "message": "Welcome to ShiftIQ API"
    }