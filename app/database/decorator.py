from contextlib import contextmanager

from sqlalchemy.orm import Session

from .db import SessionLocal


@contextmanager
def db_session_local():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def db_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def dec_session_local(func):
    def wrapper(*args, **kwargs):
        with db_session_local() as db:
            return func(db, *args, **kwargs)

    return wrapper


def dec_session(func):
    def wrapper(*args, **kwargs):
        with db_session() as db:
            return func(db, *args, **kwargs)

    return wrapper