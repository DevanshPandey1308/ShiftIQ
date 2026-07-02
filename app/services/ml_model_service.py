from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ml_model import MLModel
from app.schemas.ml_model_schema import (
    MLModelCreate,
    MLModelUpdate
)


def create_model(
    db: Session,
    model: MLModelCreate
):
    existing_model = db.query(MLModel).filter(
        MLModel.name == model.name
    ).first()

    if existing_model:
        raise HTTPException(
            status_code=400,
            detail="A model with this name already exists."
        )

    new_model = MLModel(
        name=model.name,
        description=model.description,
        problem_type=model.problem_type,
        target_column=model.target_column,
        model_type=model.model_type,

        # TODO:
        # Replace with current authenticated user's ID
        # after JWT authentication is implemented.
        owner_id=1
    )

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model


def get_all_models(db: Session):
    return db.query(MLModel).all()


def get_model_by_id(
    db: Session,
    model_id: int
):
    model = db.query(MLModel).filter(
        MLModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found."
        )

    return model


def update_model(
    db: Session,
    model_id: int,
    model_data: MLModelUpdate
):
    model = db.query(MLModel).filter(
        MLModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found."
        )

    update_data = model_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(model, key, value)

    db.commit()
    db.refresh(model)

    return model


def delete_model(
    db: Session,
    model_id: int
):
    model = db.query(MLModel).filter(
        MLModel.id == model_id
    ).first()

    if not model:
        raise HTTPException(
            status_code=404,
            detail="Model not found."
        )

    db.delete(model)
    db.commit()

    return {
        "message": "Model deleted successfully."
    }