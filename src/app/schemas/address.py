import uuid
from typing import List

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import database, models


class Address(BaseModel):
    id: uuid.UUID
    customer_id: uuid.UUID
    nickname: str
    street1: str
    street2: str
    city: str
    state: str
    zipcode: str

    @classmethod
    def id_factory(cls, customer_id: uuid.UUID, id: uuid.UUID, db: Session) -> "Address":
        item_record = (
            db.query(models.Address).filter(models.Address.customer_id == customer_id, models.Address.id == str(id)).one()
        )
        item_dict = item_record.as_dict()
        return cls(**item_dict)
   

class AddressReq(BaseModel):
    customer_id: uuid.UUID
    nickname: str
    street1: str
    street2: str
    city: str
    state: str
    zipcode: str


def list_all(customer_id: str) -> List[Address]:
    with database.session_scope() as session:
        item_records = session.query(models.Address).filter(models.Address.customer_id == customer_id).order_by(models.Address.nickname)
        recs = [Address(**rec.as_dict()) for rec in item_records]
    return recs
