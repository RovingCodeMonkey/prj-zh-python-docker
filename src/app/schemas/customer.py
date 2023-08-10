import uuid
from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import database, models


class Customer(BaseModel):
    id: uuid.UUID
    fname: str
    lname: str
    email: str

    @classmethod
    def id_factory(cls, id: uuid.UUID, db: Session) -> "Customer":
        item_record = (
            db.query(models.Customer).filter(models.Customer.id == str(id)).one()
        )
        item_dict = item_record.as_dict()
        return cls(**item_dict)
    
    @classmethod
    def email_factory(cls, email: str, db: Session) -> "Customer":
        item_record = (
            db.query(models.Customer).filter(models.Customer.email == str(email)).one_or_none()
        )
        if item_record is None:
            return None
        item_dict = item_record.as_dict()
        return cls(**item_dict)


class CustomerReq(BaseModel):
    fname: str
    lname: str
    email: str


def list_all() -> List[Customer]:
    with database.session_scope() as session:
        item_records = session.query(models.Customer).order_by(models.Customer.email).all()
        recs = [Customer(**rec.as_dict()) for rec in item_records]
    return recs
