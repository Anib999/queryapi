from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
async def login(user_credentails: schemas.UserLogin,db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentails.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Email / Password is incorrect')

    if not utils.verifyhashpassword(user_credentails.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Email / Password is incorrect')
    
    return {'token': 'asdf'}