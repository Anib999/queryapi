from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix='/query',
    tags=['Query']
)

'''Query Routes'''


@router.get('/', response_model=list[schemas.Query])
async def get_all_queries(db: Session = Depends(get_db)):
    get_queries = db.query(models.Query).all()
    print(get_queries)
    return get_queries


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_new_query(query: dict, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_query = models.Query(**query)
    db.add(new_query)
    db.commit()
    db.refresh(new_query)
    return new_query


@router.get('/GetByCompany/{company_id}', response_model=list[schemas.Query])
async def get_queries_by_company_id(company_id: int, db: Session = Depends(get_db)):
    get_related_queries = db.query(models.Query).filter(
        models.Query.company_id == company_id)

    if get_related_queries.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{company_id} not found')

    return get_related_queries.all()


@router.get('/{query_id}', response_model=schemas.Query)
async def get_single_query(query_id: int, db: Session = Depends(get_db)):
    get_query = db.query(models.Query).filter(
        models.Query.QId == query_id).first()

    if not get_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{query_id} not found')

    return get_query


@router.put('/{query_id}')
async def update_query(query_id: int, query_details: schemas.QueryUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    get_query = db.query(models.Query).filter(models.Query.QId == query_id)

    if get_query.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{query_id} not found')

    get_query.update(query_details.dict(), synchronize_session=False)
    db.commit()
    return get_query.first()
