from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix='/comment',
    tags=['Comment']
)

'''Comments Routes basically like post but included with votes or likes test'''
@router.post('/', status_code=status.HTTP_201_CREATED)
# , response_model=schemas.Comment
async def create_new_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_comment = models.Comments(**comment.dict())
    # print(new_comment)
    # return ''
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get('/', response_model=list[schemas.Comment])
async def get_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comments).all()
    return comments

@router.get('/getcommentbyqueryid/{query_id}')
async def get_comment_by_qid(query_id: int, db: Session = Depends(get_db)):
    get_all_comments_by_qid = db.query(models.Comments).filter(models.Comments.query_id == query_id).all()

    if not get_all_comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'${query_id} comments not found')
    
    return get_all_comments_by_qid

@router.put('/{comment_id}', response_model=schemas.Comment)
async def update_comment(comment: schemas.CommentCreate, comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(comment)
    get_single_comment = db.query(models.Comments).filter(models.Comments.CoId == comment_id)

    if get_single_comment.first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'${comment_id} not found')
    
    get_single_comment.update(comment.dict(), synchronize_session=False)
    db.commit()

    return get_single_comment.first()
