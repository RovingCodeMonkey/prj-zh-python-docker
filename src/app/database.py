import logging
from contextlib import contextmanager
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app import config

logger = logging.getLogger()


class _Base:
    def as_dict(self) -> Dict:
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns  # type: ignore
        }


Base = declarative_base(cls=_Base)


def get_session():  # type: ignore
    engine = create_engine(config.settings.db_uri, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


@contextmanager
def session_scope() -> Session:
    # _Session = get_session()
    session = get_session()
    try:
        yield session
        session.commit()
    except Exception as e:
        logger.error(e)
        session.rollback()
        raise
    finally:
        session.close()
