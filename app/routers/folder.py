from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import oauth2, models, schemas

router = APIRouter(
    prefix='/folder',
    tags=['Folder']
)

'''For Folders only'''


@router.get('/', response_model=list[schemas.ShowFolder])
async def get_all_folders(db: Session = Depends(get_db)):
    get_all_folder = db.query(models.Folder).all()
    return get_all_folder


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_folder(folder: schemas.FolderCreate, db: Session = Depends(get_db)):
    create_new_folder = models.Folder(**folder.dict())
    db.add(create_new_folder)
    db.commit()
    db.refresh(create_new_folder)
    return create_new_folder


@router.get('/{folder_id}', response_model=schemas.ShowFolder)
async def get_folder_by_id(folder_id: int, db: Session = Depends(get_db)):
    get_single_folder = db.query(models.Folder).filter(
        models.Folder.FId == folder_id).first()
    if not get_single_folder:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{folder_id} not found')
    return get_single_folder


@router.put('/{folder_id}', response_model=schemas.Folder)
async def update_folder(folder_id: int, folder: schemas.Folder, db: Session = Depends(get_db)):
    find_folder = db.query(models.Folder).filter(
        models.Folder.FId == folder_id)

    if find_folder.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{folder_id} not found')

    find_folder.update(folder.dict(), synchronize_session=False)
    db.commit()
    return find_folder.first()
