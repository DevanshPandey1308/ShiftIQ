import pandas as pd
from fastapi import UploadFile, HTTPException


def extract_csv_metadata(file: UploadFile):

    try:
        
        file.file.seek(0)
        
        df = pd.read_csv(file.file)

        file.file.seek(0)

        return {
            "row_count": len(df),
            "column_count": len(df.columns)
        }

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to process CSV file."
        )