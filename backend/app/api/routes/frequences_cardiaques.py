from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List
import platform


if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import FrequenceCardiaque, FrequenceCardiaqueCreate, FrequenceCardiaqueUpdate, FrequencesCardiaquesPublic, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import FrequenceCardiaque, FrequenceCardiaqueCreate, FrequenceCardiaqueUpdate, FrequencesCardiaquesPublic, Message

router = APIRouter()

@router.post("/", response_model=FrequenceCardiaque)
def create_frequence_cardiaque(frequence_cardiaque: FrequenceCardiaqueCreate, db: SessionDep):
    db_frequence_cardiaque = FrequenceCardiaque.from_orm(frequence_cardiaque)
    db.add(db_frequence_cardiaque)
    db.commit()
    db.refresh(db_frequence_cardiaque)
    return db_frequence_cardiaque

@router.get("/", response_model=FrequencesCardiaquesPublic)
def read_frequences_cardiaques(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(FrequenceCardiaque).offset(skip).limit(limit)
    results = db.exec(statement)
    frequences_cardiaques = results.all()
    return FrequencesCardiaquesPublic(data=frequences_cardiaques, count=len(frequences_cardiaques))

@router.get("/{frequence_cardiaque_id}", response_model=FrequenceCardiaque)
def read_frequence_cardiaque(frequence_cardiaque_id: int, db: SessionDep):
    frequence_cardiaque = db.get(FrequenceCardiaque, frequence_cardiaque_id)
    if frequence_cardiaque is None:
        raise HTTPException(status_code=404, detail="FrequenceCardiaque not found")
    return frequence_cardiaque

@router.put("/{frequence_cardiaque_id}", response_model=FrequenceCardiaque)
def update_frequence_cardiaque(frequence_cardiaque_id: int, frequence_cardiaque: FrequenceCardiaqueUpdate, db: SessionDep):
    db_frequence_cardiaque = db.get(FrequenceCardiaque, frequence_cardiaque_id)
    if db_frequence_cardiaque is None:
        raise HTTPException(status_code=404, detail="FrequenceCardiaque not found")
    frequence_cardiaque_data = frequence_cardiaque.dict(exclude_unset=True)
    for key, value in frequence_cardiaque_data.items():
        setattr(db_frequence_cardiaque, key, value)
    db.add(db_frequence_cardiaque)
    db.commit()
    db.refresh(db_frequence_cardiaque)
    return db_frequence_cardiaque

@router.delete("/{frequence_cardiaque_id}")
def delete_frequence_cardiaque(frequence_cardiaque_id: int, db: SessionDep) -> Message:
    db_frequence_cardiaque = db.get(FrequenceCardiaque, frequence_cardiaque_id)
    if db_frequence_cardiaque is None:
        raise HTTPException(status_code=404, detail="FrequenceCardiaque not found")
    db.delete(db_frequence_cardiaque)
    db.commit()
    return Message(message="FrequenceCardiaque deleted successfully")