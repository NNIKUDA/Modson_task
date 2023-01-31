from sqlalchemy.orm import Session

from . import models


def get_document_by_id(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()


def get_documents(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Document).offset(skip).limit(limit).all()


def remove_document_by_id(db: Session, document_id: int):
    db.query(models.Document).filter(models.Document.id == document_id).delete()
    return db.commit()

