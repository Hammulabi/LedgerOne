'''
Router Transactions - Endpoints pour la gestion des transactions
Contient tous les endpoints CRUD pour les transactions avec filtres & pagination
'''

from typing import List, Optional
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.api.dependencies import get_db
from app.models.transaction import Transaction
from app.services import (
    get_all_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction,
    get_transactions_by_period,
    search_transactions
)
from app.schemas import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/", response_model=List[TransactionResponse], status_code=status.HTTP_200_OK)
def list_transactions(
    skip:int = Query(0, ge=0),
    limit:int = Query(100, ge=1, le=500),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    category_id: Optional[int] = Query(None, ge=1),
    search: Optional[str] = Query(None, min_length=1),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=400, detail="min_amount doit être <= max_amount")

    query = db.query(Transaction)

    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))

    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query = query.filter(Transaction.date <= to_date)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    return query.order_by(Transaction.date.desc(), Transaction.id.desc()).offset(skip).limit(limit).all()

@router.get('/search-advanced', status_code=200)
def search_advanced(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
    category_id: Optional[int] = Query(None, ge=1),
    min_amount: Optional[float] = Query(None),
    max_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    if min_amount is not None and max_amount is not None and min_amount > max_amount:
        raise HTTPException(status_code=400, detail="min_amount doit être <= max_amount")

    query = db.query(Transaction)
    if search:
        query = query.filter(Transaction.description.ilike(f"%{search}%"))
    if from_date:
        query = query.filter(Transaction.date >= from_date)
    if to_date:
        query = query.filter(Transaction.date <= to_date)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    total_items = query.count()
    total_pages = max((total_items + page_size - 1) // page_size, 1)
    page = min(page, total_pages)
    items = query.order_by(Transaction.date.desc(), Transaction.id.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return {
        "items": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }

@router.get("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def get_one_transaction(transaction_id:int, db:Session = Depends(get_db)):
    transaction = get_transaction_by_id(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction avec l'ID {transaction_id} introuvable")
    return transaction

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_new_transaction(transaction_data:TransactionCreate, db:Session=Depends(get_db)):
    try:
        return create_transaction(db, transaction_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{transaction_id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def update_existing_transaction(transaction_id:int,transaction_data: TransactionUpdate,db:Session = Depends(get_db)):
    try:
        updated_transaction = update_transaction(db, transaction_id, transaction_data)
        if not updated_transaction:
            raise HTTPException(status_code=404, detail=f"Transaction avec l'ID {transaction_id} introuvable")
        return updated_transaction
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_transaction(transaction_id:int, db:Session = Depends(get_db)):
    success = delete_transaction(db, transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Transaction avec l'ID {transaction_id} introuvable")
