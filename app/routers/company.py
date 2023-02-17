from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/company',
    tags=['Company']
)

''' Company Routes '''


@router.get('/', response_model=list[schemas.Company])
async def get_company(db: Session = Depends(get_db)):
    companies = db.query(models.Company).all()
    return companies


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Company)
async def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    new_company = models.Company(**company.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@router.get('/{company_id}', response_model=schemas.Company)
async def get_company_by_id(company_id: int, db: Session = Depends(get_db)):
    get_single_company = db.query(models.Company).filter(
        models.Company.CId == company_id).first()
    if not get_single_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{company_id} not found')
    return get_single_company


@router.delete('/{company_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    get_company = db.query(models.Company).filter(
        models.Company.CId == company_id)
    if get_company.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{company_id} not found')

    get_company.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{company_id}', response_model=schemas.Company)
async def update_company(company_id: int, company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    get_company = db.query(models.Company).filter(
        models.Company.CId == company_id)

    get_single_company = get_company.first()

    if get_single_company == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{company_id} not found')

    get_company.update(company.dict(), synchronize_session=False)
    db.commit()

    return get_company.first()
