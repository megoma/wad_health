from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import platform

if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import TensionArtDebit, TensionArtDebitCreate, TensionArtDebitUpdate, TensionArtDebitsPublic, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import TensionArtDebit, TensionArtDebitCreate, TensionArtDebitUpdate, TensionArtDebitsPublic, Message

router = APIRouter()

@router.post("/", response_model=TensionArtDebit)
def create_tension_art_debit(tension_art_debit: TensionArtDebitCreate, db: SessionDep):
    db_tension_art_debit = TensionArtDebit.from_orm(tension_art_debit)
    db.add(db_tension_art_debit)
    db.commit()
    db.refresh(db_tension_art_debit)
    return db_tension_art_debit

@router.get("/", response_model=TensionArtDebitsPublic)
def read_tension_art_debits(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(TensionArtDebit).offset(skip).limit(limit)
    results = db.exec(statement)
    tension_art_debits = results.all()
    return TensionArtDebitsPublic(data=tension_art_debits, count=len(tension_art_debits))

@router.get("/{tension_art_debit_id}", response_model=TensionArtDebit)
def read_tension_art_debit(tension_art_debit_id: int, db: SessionDep):
    tension_art_debit = db.get(TensionArtDebit, tension_art_debit_id)
    if tension_art_debit is None:
        raise HTTPException(status_code=404, detail="TensionArtDebit not found")
    return tension_art_debit

@router.put("/{tension_art_debit_id}", response_model=TensionArtDebit)
def update_tension_art_debit(tension_art_debit_id: int, tension_art_debit: TensionArtDebitUpdate, db: SessionDep):
    db_tension_art_debit = db.get(TensionArtDebit, tension_art_debit_id)
    if db_tension_art_debit is None:
        raise HTTPException(status_code=404, detail="TensionArtDebit not found")
    tension_art_debit_data = tension_art_debit.dict(exclude_unset=True)
    for key, value in tension_art_debit_data.items():
        setattr(db_tension_art_debit, key, value)
    db.add(db_tension_art_debit)
    db.commit()
    db.refresh(db_tension_art_debit)
    return db_tension_art_debit

@router.delete("/{tension_art_debit_id}")
def delete_tension_art_debit(tension_art_debit_id: int, db: SessionDep) -> Message:
    db_tension_art_debit = db.get(TensionArtDebit, tension_art_debit_id)
    if db_tension_art_debit is None:
        raise HTTPException(status_code=404, detail="TensionArtDebit not found")
    db.delete(db_tension_art_debit)
    db.commit()
    return Message(message="TensionArtDebit deleted successfully")