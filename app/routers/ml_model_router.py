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

from fastapi import UploadFile, File, Form

from app.services.dataset_service import (
    register_baseline_dataset,
    register_batch_dataset
)

from app.schemas.dataset_schema import (
    DatasetResponse
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

@router.post(
    "/{model_id}/baseline",
    response_model=DatasetResponse,
    status_code=201
)

def upload_baseline_dataset(
    model_id: int,
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return register_baseline_dataset(
        db=db,
        model_id=model_id,
        name=name,
        file=file
    )

@router.post(
    "/{model_id}/batch",
    response_model=DatasetResponse,
    status_code=201
)
def upload_batch_dataset(
    model_id: int,
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    return register_batch_dataset(
        db=db,
        model_id=model_id,
        name=name,
        file=file
    )