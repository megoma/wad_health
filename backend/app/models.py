from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional
from datetime import datetime


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class ChurchUnionBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(max_length=255)
    website: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

class ChurchUnionCreate(ChurchUnionBase):
    pass

class ChurchUnionUpdate(ChurchUnionBase):
    pass

class ChurchUnion(ChurchUnionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conferences: List["Conference"] = Relationship(back_populates="church_union")

class ChurchUnionsPublic(SQLModel):
    data: list[ChurchUnion]
    count: int


class ConferenceBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(max_length=255)
    website: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    church_union_id: int = Field(foreign_key="churchunion.id", nullable=False)

class ConferenceCreate(ConferenceBase):
    pass

class ConferenceUpdate(ConferenceBase):
    pass

class Conference(ConferenceBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    church_union: ChurchUnion | None = Relationship(back_populates="conferences")
    districts: List["District"] = Relationship(back_populates="conference")

class ConferencesPublic(SQLModel):
    data: list[Conference]
    count: int


class DistrictBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(max_length=255)
    website: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    conference_id: int = Field(foreign_key="conference.id", nullable=False)

class DistrictCreate(DistrictBase):
    pass

class DistrictUpdate(DistrictBase):
    pass

class District(DistrictBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conference: Conference | None = Relationship(back_populates="districts")
    churches: List["Church"] = Relationship(back_populates="district")

class DistrictsPublic(SQLModel):
    data: list[District]
    count: int


class ChurchBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    phone_number: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(max_length=255)
    website: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)

class ChurchCreate(ChurchBase):
    pass

class ChurchUpdate(ChurchBase):
    pass

class Church(ChurchBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    members : List["ChurchMember"] = Relationship(back_populates="church")

    district_id: int = Field(foreign_key="district.id", nullable=False)
    district: District = Relationship(back_populates="churches")

class ChurchesPublic(SQLModel):
    data: list[Church]
    count: int


class ChurchMemberBase(SQLModel):
    full_name: str = Field(min_length=1, max_length=255)
    email: EmailStr = Field(max_length=255)
    phone_number: str = Field(min_length=1, max_length=255)
    address: str = Field(min_length=1, max_length=255)
    church_id: int = Field(foreign_key="church.id", nullable=False)

class ChurchMemberCreate(ChurchMemberBase):
    pass

class ChurchMemberUpdate(ChurchMemberBase):
    pass

class ChurchMember(ChurchMemberBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    church: Church | None = Relationship(back_populates="members")

    tensions: List["TensionArtDebit"] = Relationship(back_populates="member")
    glycemies: List["Glycemie"] = Relationship(back_populates="member")
    poids: List["Poids"] = Relationship(back_populates="member")
    frequences_cardiaques: List["FrequenceCardiaque"] = Relationship(back_populates="member")
    cholesterols: List["Cholesterol"] = Relationship(back_populates="member")
    imcs: List["IMC"] = Relationship(back_populates="member")
    hemoglobines: List["Hemoglobine"] = Relationship(back_populates="member")
    pressions_oculaires: List["PressionOculaire"] = Relationship(back_populates="member")
    activites: List["ActivitePhysique"] = Relationship(back_populates="member")
    sommeils: List["Sommeil"] = Relationship(back_populates="member")
    stress: List["Stress"] = Relationship(back_populates="member")
    nutriments: List["Nutriments"] = Relationship(back_populates="member")

class ChurchMembersPublic(SQLModel):
    data: list[ChurchMember]
    count: int


class TensionArtDebitBase(SQLModel):
    date_mesure: datetime
    tension_systolique: int
    tension_diastolique: int
    id_member: int = Field(foreign_key="churchmember.id")

class TensionArtDebitCreate(TensionArtDebitBase):
    pass

class TensionArtDebitUpdate(TensionArtDebitBase):
    pass

class TensionArtDebit(TensionArtDebitBase, table=True):
    id_tension: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="tensions")

class TensionArtDebitsPublic(SQLModel):
    data: list[TensionArtDebit]
    count: int

class GlycemieBase(SQLModel):
    date_mesure: datetime
    valeur: float
    id_member: int = Field(foreign_key="churchmember.id")

class GlycemieCreate(GlycemieBase):
    pass

class GlycemieUpdate(GlycemieBase):
    pass

class Glycemie(GlycemieBase, table=True):
    id_glycemie: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="glycemies")

class GlycemiesPublic(SQLModel):
    data: list[Glycemie]
    count: int

class PoidsBase(SQLModel):
    date_mesure: datetime
    poids: float
    id_member: int = Field(foreign_key="churchmember.id")

class PoidsCreate(PoidsBase):
    pass

class PoidsUpdate(PoidsBase):
    pass

class Poids(PoidsBase, table=True):
    id_poids: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="poids")

class FrequenceCardiaqueBase(SQLModel):
    date_mesure: datetime
    frequence: int  # en battements par minute
    id_member: int = Field(foreign_key="churchmember.id")

class FrequenceCardiaqueCreate(FrequenceCardiaqueBase):
    pass

class FrequenceCardiaqueUpdate(FrequenceCardiaqueBase):
    pass

class FrequenceCardiaque(FrequenceCardiaqueBase, table=True):
    id_frequence: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="frequences_cardiaques")

class FrequencesCardiaquesPublic(SQLModel):
    data: list[FrequenceCardiaque]
    count: int


class CholesterolBase(SQLModel):
    date_mesure: datetime
    ldl: float  # LDL cholesterol
    hdl: float  # HDL cholesterol
    triglycérides: float
    id_member: int = Field(foreign_key="churchmember.id")

class CholesterolCreate(CholesterolBase):
    pass

class CholesterolUpdate(CholesterolBase):
    pass

class Cholesterol(CholesterolBase, table=True):
    id_cholesterol: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="cholesterols")

class CholesterolsPublic(SQLModel):
    data: list[Cholesterol]
    count: int


class IMCBase(SQLModel):
    date_mesure: datetime
    imc: float  # Calculé comme poids / (taille^2)
    id_member: int = Field(foreign_key="churchmember.id")

class IMCCreate(IMCBase):
    pass

class IMCUpdate(IMCBase):
    pass

class IMC(IMCBase, table=True):
    id_imc: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="imcs")

class IMCsPublic(SQLModel):
    data: list[IMC]
    count: int

class HemoglobineBase(SQLModel):
    date_mesure: datetime
    taux: float  # en g/dL
    id_member: int = Field(foreign_key="churchmember.id")

class HemoglobineCreate(HemoglobineBase):
    pass

class HemoglobineUpdate(HemoglobineBase):
    pass

class Hemoglobine(HemoglobineBase, table=True):
    id_hemoglobine: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="hemoglobines")

class HemoglobinesPublic(SQLModel):
    data: list[Hemoglobine]
    count: int

class PressionOculaireBase(SQLModel):
    date_mesure: datetime
    pression: float  # en mmHg
    id_member: int = Field(foreign_key="churchmember.id")

class PressionOculaireCreate(PressionOculaireBase):
    pass

class PressionOculaireUpdate(PressionOculaireBase):
    pass

class PressionOculaire(PressionOculaireBase, table=True):
    id_pression: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="pressions_oculaires")

class PressionsOculairesPublic(SQLModel):
    data: list[PressionOculaire]
    count: int

class ActivitePhysiqueBase(SQLModel):
    date_mesure: datetime
    type_activite: str = Field(min_length=1, max_length=255)  # type d'activité (ex. marche, course, etc.)
    duree: int  # durée en minutes
    id_member: int = Field(foreign_key="churchmember.id")

class ActivitePhysiqueCreate(ActivitePhysiqueBase):
    pass

class ActivitePhysiqueUpdate(ActivitePhysiqueBase):
    pass

class ActivitePhysique(ActivitePhysiqueBase, table=True):
    id_activite: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="activites")

class ActivitesPhysiquesPublic(SQLModel):
    data: list[ActivitePhysique]
    count: int

class SommeilBase(SQLModel):
    date_mesure: datetime
    duree: int  # durée en heures
    qualite: str = Field(min_length=1, max_length=255)  # évaluation de la qualité (ex. bonne, moyenne, mauvaise)
    id_member: int = Field(foreign_key="churchmember.id")

class SommeilCreate(SommeilBase):
    pass

class SommeilUpdate(SommeilBase):
    pass

class Sommeil(SommeilBase, table=True):
    id_sommeil: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="sommeils")

class SommeilsPublic(SQLModel):
    data: list[Sommeil]
    count: int

class StressBase(SQLModel):
    date_mesure: datetime
    niveau: int  # échelle de 1 à 10
    id_member: int = Field(foreign_key="churchmember.id")

class StressCreate(StressBase):
    pass

class StressUpdate(StressBase):
    pass

class Stress(StressBase, table=True):
    id_stress: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="stress")

class StressesPublic(SQLModel):
    data: list[Stress]
    count: int

class NutrimentsBase(SQLModel):
    date_mesure: datetime
    vitamine_d: float  # en ng/mL
    fer: float  # en µg/dL
    calcium: float  # en mg/dL
    id_member: int = Field(foreign_key="churchmember.id")

class NutrimentsCreate(NutrimentsBase):
    pass

class NutrimentsUpdate(NutrimentsBase):
    pass

class Nutriments(NutrimentsBase, table=True):
    id_nutriment: Optional[int] = Field(default=None, primary_key=True)
    member: ChurchMember = Relationship(back_populates="nutriments")

class NutrimentsPublic(SQLModel):
    data: list[Nutriments]
    count: int