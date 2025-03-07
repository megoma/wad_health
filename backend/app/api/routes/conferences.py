from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select

import platform
if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import Conference, ConferenceCreate, ConferenceUpdate, Message
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import Conference, ConferenceCreate, ConferenceUpdate, Message

router = APIRouter()

@router.post("/", response_model=Conference)
def create_conference(conference: ConferenceCreate, db: SessionDep):
    db_conference = Conference.from_orm(conference)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference

@router.get("/", response_model=List[Conference])
def read_conferences(db: SessionDep, skip: int = 0, limit: int = 10):
    statement = select(Conference).offset(skip).limit(limit)
    results = db.exec(statement)
    conferences = results.all()
    return conferences

@router.get("/{conference_id}", response_model=Conference)
def read_conference(conference_id: int, db: SessionDep):
    conference = db.get(Conference, conference_id)
    if conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    return conference

@router.put("/{conference_id}", response_model=Conference)
def update_conference(conference_id: int, conference: ConferenceUpdate, db: SessionDep):
    db_conference = db.get(Conference, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    conference_data = conference.dict(exclude_unset=True)
    for key, value in conference_data.items():
        setattr(db_conference, key, value)
    db.add(db_conference)
    db.commit()
    db.refresh(db_conference)
    return db_conference

@router.delete("/{conference_id}")
def delete_conference(conference_id: int, db: SessionDep) -> Message:
    db_conference = db.get(Conference, conference_id)
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    db.delete(db_conference)
    db.commit()
    return Message(message="Conference deleted successfully")
