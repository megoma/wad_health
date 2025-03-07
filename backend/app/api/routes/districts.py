from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import platform

if platform.system() in ["Windows"]:
    from api.deps import CurrentUser, SessionDep
    from models import District, DistrictCreate, DistrictUpdate, DistrictsPublic
else:
    from app.api.deps import CurrentUser, SessionDep
    from app.models import District, DistrictCreate, DistrictUpdate, DistrictsPublic

router = APIRouter()

@router.post("/", response_model=District)
def create_district(district: DistrictCreate, db: SessionDep):
    db_district = District(**district.dict())
    db.add(db_district)
    db.commit()
    db.refresh(db_district)
    return db_district

@router.get("/", response_model=DistrictsPublic)
def read_districts(db: SessionDep, skip: int = 0, limit: int = 10):
    districts = db.query(District).offset(skip).limit(limit).all()
    total_count = db.query(District).count()
    return DistrictsPublic(districts=districts, count=total_count)

@router.get("/{district_id}", response_model=District)
def read_district(district_id: int, db: SessionDep):
    district = db.query(District).filter(District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    return district

@router.put("/{district_id}", response_model=District)
def update_district(district_id: int, district: DistrictUpdate, db: SessionDep):
    db_district = db.query(District).filter(District.id == district_id).first()
    if db_district is None:
        raise HTTPException(status_code=404, detail="District not found")
    for key, value in district.dict().items():
        setattr(db_district, key, value)
    db.commit()
    db.refresh(db_district)
    return db_district

@router.delete("/{district_id}", response_model=District)
def delete_district(district_id: int, db: SessionDep):
    district = db.query(District).filter(District.id == district_id).first()
    if district is None:
        raise HTTPException(status_code=404, detail="District not found")
    db.delete(district)
    db.commit()
    return district
