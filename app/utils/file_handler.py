import os
import shutil
import uuid
import csv
import io

from fastapi import UploadFile, HTTPException

UPLOAD_FOLDER = "uploads"


def validate_csv(file: UploadFile):

    # Move pointer to the beginning
    file.file.seek(0)

    try:
        # Read file content
        content = file.file.read().decode("utf-8")

        # Parse CSV
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)

        # Check if CSV has at least header + one row
        if len(rows) < 2:
            raise HTTPException(
                status_code=400,
                detail="CSV must contain headers and at least one data row."
            )

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV must be UTF-8 encoded."
        )

    except csv.Error:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV format."
        )

    finally:
        # Reset pointer so the file can be saved afterwards
        file.file.seek(0)


def save_uploaded_file(file: UploadFile) -> str:

    # Allow only CSV files
    if file.content_type != "text/csv":
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    # Validate CSV content
    validate_csv(file)

    # Create uploads folder if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"

    # Full file path
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path