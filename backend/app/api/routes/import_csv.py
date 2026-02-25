'''
Router Import CSV - Endpoint pour l'import en masse de transactions
Expose l'endpoint POST /api/import/csv pour uploader et traiter fichier CSV
'''

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services.import_service import import_transactions_from_csv
from app.utils.csv_parser import parse_csv_content

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/preview", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def preview_csv(file: UploadFile = File(...), max_rows: int = 5):
    if not file or not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV (.csv)")

    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Le fichier est vide")

    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="Le fichier doit être encodé en UTF-8") from exc

    rows, delimiter, errors = parse_csv_content(decoded)
    return {
        "detected_delimiter": delimiter,
        "preview_rows": rows[:max_rows],
        "total_rows": len(rows),
        "errors": errors,
    }


@router.post("/csv", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
async def import_csv(
    file: UploadFile = File(..., description="Fichier CSV contenant les transactions à importer"),
    db: Session = Depends(get_db),
):
    if not file:
        raise HTTPException(status_code=400, detail="Aucun fichier n'a été fourni")
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Le fichier doit être au format CSV (.csv)")

    file_content = await file.read()
    if not file_content:
        raise HTTPException(status_code=400, detail="Le fichier est vide")

    try:
        return import_transactions_from_csv(db, file_content)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'import : {str(e)}")
