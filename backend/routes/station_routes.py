from fastapi import APIRouter
router = APIRouter(prefix='/api/stations', tags=['Stations'])

@router.get('')
def list_stations():
    return [{'id': 'ST-01', 'name': 'Amer Fort Ridge', 'active': True}]
