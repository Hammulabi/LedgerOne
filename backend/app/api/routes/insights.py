'''
Router Insights - Endpoints pour les statistiques et analyses
Contient tous les endpoints pour récupérer agrégations et analyses de dépenses
'''
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import extract, func

from app.api.dependencies import get_db
from app.models.transaction import Transaction
from app.services import (get_monthly_total, get_category_breakdown, get_monthly_summary)

router = APIRouter(prefix="/insights", tags=["Insights"])

@router.get("/summary", response_model=Dict[str, Any],status_code=status.HTTP_200_OK)
def get_month_summary(year:int = Query(..., ge=2000, le=2100), month:int = Query(..., ge=1, le=12), db:Session = Depends(get_db)):
    try:
        return get_monthly_summary(db, year, month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul du résumé: {str(e)}")

@router.get("/monthly-total", response_model=Dict[str, float], status_code=status.HTTP_200_OK)
def get_month_total(year:int = Query(..., ge=2000, le=2100), month:int = Query(..., ge=1, le=12), category_id:int = Query(None, ge=1), db:Session = Depends(get_db)):
    try:
        return {"total": get_monthly_total(db, year, month, category_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul du total: {str(e)}")

@router.get("/category-breakdown", response_model=Dict[str, Dict[str, Any]], status_code = status.HTTP_200_OK)
def get_breakdown_by_category(year:int = Query(..., ge=2000, le=2100), month:int = Query(..., ge=1, le=12), db:Session = Depends(get_db)):
    try:
        return get_category_breakdown(db, year, month)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du calcul de la répartition: {str(e)}")

@router.get('/annual-expenses', response_model=Dict[str, Any], status_code=200)
def annual_expenses(year: int = Query(..., ge=2000, le=2100), db: Session = Depends(get_db)):
    monthly_rows = db.query(
        extract('month', Transaction.date).label('month'),
        func.sum(Transaction.amount).label('total')
    ).filter(extract('year', Transaction.date) == year).group_by(extract('month', Transaction.date)).all()

    month_totals = {int(m): float(t or 0) for m, t in monthly_rows}
    months = [{"month": m, "total": round(month_totals.get(m, 0.0), 2)} for m in range(1, 13)]
    return {"year": year, "total": round(sum(x["total"] for x in months), 2), "months": months}

@router.get('/monthly-evolution', response_model=Dict[str, Any], status_code=200)
def monthly_evolution(year: int = Query(..., ge=2000, le=2100), month: int = Query(..., ge=1, le=12), db: Session = Depends(get_db)):
    current_total = get_monthly_total(db, year, month)
    prev_year = year if month > 1 else year - 1
    prev_month = month - 1 if month > 1 else 12
    previous_total = get_monthly_total(db, prev_year, prev_month)

    if previous_total == 0:
        change_percent = 100.0 if current_total > 0 else 0.0
    else:
        change_percent = ((current_total - previous_total) / previous_total) * 100

    return {
        "current_total": round(current_total, 2),
        "previous_total": round(previous_total, 2),
        "change_percent": round(change_percent, 2),
        "is_increase": change_percent > 0,
    }

@router.get('/savings-goal', response_model=Dict[str, Any], status_code=200)
def savings_goal(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    income: float = Query(..., gt=0),
    goal: float = Query(..., ge=0),
    db: Session = Depends(get_db),
):
    expenses = get_monthly_total(db, year, month)
    current_savings = max(income - expenses, 0)
    completion_rate = 100.0 if goal == 0 else min((current_savings / goal) * 100, 100.0)
    return {
        "income": round(income, 2),
        "goal": round(goal, 2),
        "expenses": round(expenses, 2),
        "current_savings": round(current_savings, 2),
        "completion_rate": round(completion_rate, 2),
        "remaining": round(max(goal - current_savings, 0), 2),
    }
