from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
# from app.models import ChurchUnion, ChurchUnionCreate, ChurchUnionUpdate

import platform
if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import ChurchUnion, ChurchUnionCreate, ChurchUnionUpdate, ChurchUnionsPublic, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import ChurchUnion, ChurchUnionCreate, ChurchUnionUpdate, ChurchUnionsPublic, Message


router = APIRouter()

@router.post("/", response_model=ChurchUnion)
def create_church_union(church_union: ChurchUnionCreate, db: SessionDep):
    db_church_union = ChurchUnion.from_orm(church_union)
    db.add(db_church_union)
    db.commit()
    db.refresh(db_church_union)
    return db_church_union

@router.get("/", response_model=ChurchUnionsPublic)
def read_church_unions(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(ChurchUnion).offset(skip).limit(limit)
    results = db.exec(statement)
    church_unions = results.all()
    return ChurchUnionsPublic(data=church_unions, count=len(church_unions))

@router.get("/{church_union_id}", response_model=ChurchUnion)
def read_church_union(church_union_id: int, db: SessionDep):
    church_union = db.get(ChurchUnion, church_union_id)
    if church_union is None:
        raise HTTPException(status_code=404, detail="ChurchUnion not found")
    return church_union

@router.put("/{church_union_id}", response_model=ChurchUnion)
def update_church_union(church_union_id: int, church_union: ChurchUnionUpdate, db: SessionDep):
    db_church_union = db.get(ChurchUnion, church_union_id)
    if db_church_union is None:
        raise HTTPException(status_code=404, detail="ChurchUnion not found")
    church_union_data = church_union.dict(exclude_unset=True)
    for key, value in church_union_data.items():
        setattr(db_church_union, key, value)
    db.add(db_church_union)
    db.commit()
    db.refresh(db_church_union)
    return db_church_union

@router.delete("/{church_union_id}")
def delete_church_union(church_union_id: int, db: SessionDep) -> Message:
    db_church_union = db.get(ChurchUnion, church_union_id)
    if db_church_union is None:
        raise HTTPException(status_code=404, detail="ChurchUnion not found")
    db.delete(db_church_union)
    db.commit()
    return Message(message="ChurchUnion deleted successfully")