from fastapi import HTTPException, APIRouter, status, Depends
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)


@router.post('/login')
async def login(user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Email / Password is incorrect')

    if not utils.verifyhashpassword(user_credentails.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Email / Password is incorrect')

    payload_data = {'user_id': user.UId}
    access_token = oauth2.create_access_token(data=payload_data)

    return {'access_token': access_token, 'token_type': 'bearer'}
