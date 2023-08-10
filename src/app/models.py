from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Customer(Base):  # type: ignore
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    fname = Column(String)
    lname = Column(String)
    fname = Column(String)
    email = Column(String)
    UniqueConstraint("email",  name="uix_1")

class Address(Base):  # type: ignore
    __tablename__ = "addresses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey(Customer.id), default=uuid4)
    nickname = Column(String)
    street1 = Column(String)
    street2 = Column(String)
    city = Column(String)
    state = Column(String)
    zipcode = Column(String)
    customer = relationship("Customer", back_populates = "addresses")
    UniqueConstraint("customer_id", "street1", "street2", "city", "state", "zipcode",  name="uix_1")

Customer.addresses = relationship("Address", order_by = Address.nickname, back_populates = "customer")