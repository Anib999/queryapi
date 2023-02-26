from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, oauth2

router = APIRouter(
    prefix='/like',
    tags=['Likes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_like(like_details: schemas.LikeCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    comment_detail = db.query(models.Comments).filter(
        models.Comments.CoId == like_details.comment_id).first()

    if not comment_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Comment Not found')

    like_query = db.query(models.Likes).filter(models.Likes.comment_id ==
                                               like_details.comment_id, models.Likes.user_id == current_user.UId)
    found_like = like_query.first()

    if like_details.comment_dir == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'{current_user.UId} has already liked {like_details.comment_id} comment.')
        new_like = models.Likes(user_id=current_user.UId,
                                comment_id=like_details.comment_id)
        db.add(new_like)
        db.commit()
        return {'message': 'Liked'}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'{like_details.comment_id} not found')
        like_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'unliked'}


@router.get('/')
async def get_all_likes(db: Session = Depends(get_db)):
    get_likes = db.query(models.Likes).all()
    return get_likes


@router.get('/likecount')
async def get_like_count(db: Session = Depends(get_db)):
    get_count = db.query(models.Comments, func.count(models.Likes.comment_id).label('LikeCount')).join(
        models.Likes, models.Comments.CoId == models.Likes.comment_id, isouter=True).group_by(models.Comments.CoId)
    print(get_count)
    return get_count.all()
