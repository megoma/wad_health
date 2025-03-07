from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import platform

if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import Church, ChurchCreate, ChurchUpdate, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import Church, ChurchCreate, ChurchUpdate, Message

router = APIRouter()

@router.post("/", response_model=Church)
def create_church(church: ChurchCreate, db: SessionDep):
    db_church = Church.from_orm(church)
    db.add(db_church)
    db.commit()
    db.refresh(db_church)
    return db_church

@router.get("/", response_model=List[Church])
def read_churches(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(Church).offset(skip).limit(limit)
    results = db.exec(statement)
    churches = results.all()
    return churches

@router.get("/{church_id}", response_model=Church)
def read_church(church_id: int, db: SessionDep):
    church = db.get(Church, church_id)
    if church is None:
        raise HTTPException(status_code=404, detail="Church not found")
    return church

@router.put("/{church_id}", response_model=Church)
def update_church(church_id: int, church: ChurchUpdate, db: SessionDep):
    db_church = db.get(Church, church_id)
    if db_church is None:
        raise HTTPException(status_code=404, detail="Church not found")
    church_data = church.dict(exclude_unset=True)
    for key, value in church_data.items():
        setattr(db_church, key, value)
    db.add(db_church)
    db.commit()
    db.refresh(db_church)
    return db_church

@router.delete("/{church_id}")
def delete_church(church_id: int, db: SessionDep) -> Message:
    db_church = db.get(Church, church_id)
    if db_church is None:
        raise HTTPException(status_code=404, detail="Church not found")
    db.delete(db_church)
    db.commit()
    return Message(message="Church deleted successfully")