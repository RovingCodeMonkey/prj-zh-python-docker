import logging
from typing import List

from fastapi import APIRouter, HTTPException
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from app import database, models, utils
from app.models import Address
from app.schemas import address

logger = logging.getLogger()

router = APIRouter(prefix="/customers/{customer_id}/addresses", tags=["Addresses"])


@router.get("/{id}", response_model=address.Address)
async def get_address(customer_id:str, id: str) -> utils.JSONResponse:
    if not utils.validate_uuid(id):
        raise HTTPException(status_code=404, detail="item not found")

    try:
        db = database.get_session()
        return utils.JSONResponse(
            content=address.Address.id_factory(customer_id, id, db).dict(by_alias=True)
        )

    except NoResultFound:
        raise HTTPException(status_code=404, detail="item not found")


@router.get("/", response_model=List[address.Address])
async def list_addresses(customer_id: str) -> utils.JSONResponse:
    items = [_i.dict(by_alias=True) for _i in address.list_all(customer_id)]
    return utils.JSONResponse(content=items)


@router.post("/", response_model=address.Address)
async def post_address(customer_id: str, address_req: address.AddressReq) -> utils.JSONResponse:
    try:
        db = database.get_session()
        record = models.Address(**address_req.dict())
        db.add(record)
        db.commit()
        return utils.JSONResponse(content=record.as_dict())
    # Catch unique key constraint and return as 422
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Address already exists")
        


@router.patch("/{id}", response_model=address.Address)
async def patch_address(
    customer_id: str, id: str, address_req: address.AddressReq
) -> utils.JSONResponse:
    try:
        db = database.get_session()
        
        record = db.query(Address).filter_by(id=id).one_or_none()

        if record is None:
            raise HTTPException(status_code=404, detail="item not found")

        for k, v in address_req.dict().items():
            setattr(record, k, str(v))

        db.add(record)
        db.commit()
        return utils.JSONResponse(content=record.as_dict())
    # Catch unique key constraint error and return as 422
    except IntegrityError:
        raise HTTPException(status_code=422, detail="Address already exists")

@router.delete("/{id}", response_model=address.Address)
async def delete_address(customer_id: str, id: str) -> utils.JSONResponse:
    if not utils.validate_uuid(id):
        raise HTTPException(status_code=400, detail="bad request - not a valid item_id")

    with database.session_scope() as session:
        item_rec = session.query(models.Address).filter_by(customer_id=str(customer_id),id=str(id)).one()
        session.delete(item_rec)

    addresses = [_i.dict(by_alias=True) for _i in address.list_all(customer_id)]
    return utils.JSONResponse(content=addresses)
