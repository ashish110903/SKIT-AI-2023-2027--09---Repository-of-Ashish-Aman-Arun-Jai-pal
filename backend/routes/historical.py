from fastapi import APIRouter
from datetime import date
router = APIRouter(prefix='/api/historical', tags=['Historical'])

@router.get('/query')
def query_history(start: date, end: date):
    return {'count': 0, 'range': f'{start} to {end}'}
