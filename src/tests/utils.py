from sqlalchemy.orm import Session

from app import models


def test_item(session: Session) -> None:
    # insert example item
    customer_row = models.Customer(
        fname="Marco",
        lname="Fonseca",
        email="marco@test.com"
    )
    session.add(customer_row)
    session.commit()

