import logging
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.exc import NoResultFound

from app import database, models, utils
from app.models import Customer
from app.schemas import customer

logger = logging.getLogger()

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("/{id}", response_model=customer.Customer)
async def get_customer(id: str) -> utils.JSONResponse:
    if not utils.validate_uuid(id):
        raise HTTPException(status_code=404, detail="item not found")

    try:
        db = database.get_session()
        return utils.JSONResponse(
            content=customer.Customer.id_factory(id, db).dict(by_alias=True)
        )

    except NoResultFound:
        raise HTTPException(status_code=404, detail="item not found")


@router.get("/", response_model=List[customer.Customer])
async def list_customers() -> utils.JSONResponse:
    items = [_i.dict(by_alias=True) for _i in customer.list_all()]
    return utils.JSONResponse(content=items)


@router.post("/", response_model=customer.Customer)
async def post_customer(customer_req: customer.CustomerReq) -> utils.JSONResponse:
    db = database.get_session()
    email_record = customer.Customer.email_factory(customer_req.email, db)
    #Verify email is unique.
    if email_record is not None:
        raise HTTPException(status_code=422, detail="Email already exists")
    record = models.Customer(**customer_req.dict())
    db.add(record)
    db.commit()
    return utils.JSONResponse(content=record.as_dict())


@router.patch("/{id}", response_model=customer.Customer)
async def patch_customer(
    id: str, customer_req: customer.CustomerReq
) -> utils.JSONResponse:
    db = database.get_session()
    
    #Verify email is unique. Ignore if it's this users record
    email_record = customer.Customer.email_factory(customer_req.email, db)
    if email_record is not None and str(email_record.id) != id:
        raise HTTPException(status_code=422, detail="Email already exists")
    
    record = db.query(Customer).filter_by(id=id).one_or_none()

    if record is None:
        raise HTTPException(status_code=404, detail="item not found")

    for k, v in customer_req.dict().items():
        setattr(record, k, str(v))

    db.add(record)
    db.commit()
    return utils.JSONResponse(content=record.as_dict())


@router.delete("/{id}", response_model=customer.Customer)
async def delete_customer(id: str) -> utils.JSONResponse:
    if not utils.validate_uuid(id):
        raise HTTPException(status_code=400, detail="bad request - not a valid item_id")

    with database.session_scope() as session:
        item_rec = session.query(models.Customer).filter_by(id=str(id)).one()
        session.delete(item_rec)

    customers = [_i.dict(by_alias=True) for _i in customer.list_all()]
    return utils.JSONResponse(content=customers)
