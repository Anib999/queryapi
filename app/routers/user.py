from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/users',
    tags=['Users']
)


''' User Routes '''


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = utils.hashpassword(user.password)
    create_new_user = models.User(**user.dict())
    db.add(create_new_user)
    db.commit()
    db.refresh(create_new_user)
    return create_new_user


@router.get('/', response_model=list[schemas.User])
async def get_all_users(db: Session = Depends(get_db)):
    all_users = db.query(models.User).all()
    return all_users


@router.get('/{user_id}', response_model=schemas.User)
async def get_single_user(user_id: int, db: Session = Depends(get_db)):
    get_one_user = db.query(models.User).filter(
        models.User.UId == user_id).first()

    if get_one_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{user_id} not found')
    return get_one_user


@router.put('/{user_id}', response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.UId == user_id)

    get_one_user = get_user.first()

    if get_one_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{user_id} not found')

    get_user.update(**user.dict(), synchronize_session=False)
    db.commit()

    return get_user.first()


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    get_user = db.query(models.User).filter(models.User.UId == user_id)

    get_one_user = get_user.first()

    if get_one_user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'{user_id} not found')

    get_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
