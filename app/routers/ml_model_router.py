from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.ml_model_schema import (
    MLModelCreate,
    MLModelUpdate,
    MLModelResponse
)

from app.services.ml_model_service import (
    create_model,
    get_all_models,
    get_model_by_id,
    update_model,
    delete_model
)

router = APIRouter(
    prefix="/models",
    tags=["ML Models"]
)


@router.post("/", response_model=MLModelResponse)
def register_model(
    model: MLModelCreate,
    db: Session = Depends(get_db)
):
    return create_model(db, model)


@router.get("/", response_model=list[MLModelResponse])
def read_all_models(
    db: Session = Depends(get_db)
):
    return get_all_models(db)


@router.get("/{model_id}", response_model=MLModelResponse)
def read_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    return get_model_by_id(db, model_id)


@router.put("/{model_id}", response_model=MLModelResponse)
def update_existing_model(
    model_id: int,
    model: MLModelUpdate,
    db: Session = Depends(get_db)
):
    return update_model(
        db,
        model_id,
        model
    )


@router.delete("/{model_id}")
def delete_existing_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    return delete_model(
        db,
        model_id
    )