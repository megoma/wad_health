from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import platform

if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import Glycemie, GlycemieCreate, GlycemieUpdate, GlycemiesPublic, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import Glycemie, GlycemieCreate, GlycemieUpdate, GlycemiesPublic, Message

router = APIRouter()

@router.post("/", response_model=Glycemie)
def create_glycemie(glycemie: GlycemieCreate, db: SessionDep):
    db_glycemie = Glycemie.from_orm(glycemie)
    db.add(db_glycemie)
    db.commit()
    db.refresh(db_glycemie)
    return db_glycemie

@router.get("/", response_model=GlycemiesPublic)
def read_glycemies(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(Glycemie).offset(skip).limit(limit)
    results = db.exec(statement)
    glycemies = results.all()
    return GlycemiesPublic(data=glycemies, count=len(glycemies))

@router.get("/{glycemie_id}", response_model=Glycemie)
def read_glycemie(glycemie_id: int, db: SessionDep):
    glycemie = db.get(Glycemie, glycemie_id)
    if glycemie is None:
        raise HTTPException(status_code=404, detail="Glycemie not found")
    return glycemie

@router.put("/{glycemie_id}", response_model=Glycemie)
def update_glycemie(glycemie_id: int, glycemie: GlycemieUpdate, db: SessionDep):
    db_glycemie = db.get(Glycemie, glycemie_id)
    if db_glycemie is None:
        raise HTTPException(status_code=404, detail="Glycemie not found")
    glycemie_data = glycemie.dict(exclude_unset=True)
    for key, value in glycemie_data.items():
        setattr(db_glycemie, key, value)
    db.add(db_glycemie)
    db.commit()
    db.refresh(db_glycemie)
    return db_glycemie

@router.delete("/{glycemie_id}")
def delete_glycemie(glycemie_id: int, db: SessionDep) -> Message:
    db_glycemie = db.get(Glycemie, glycemie_id)
    if db_glycemie is None:
        raise HTTPException(status_code=404, detail="Glycemie not found")
    db.delete(db_glycemie)
    db.commit()
    return Message(message="Glycemie deleted successfully")