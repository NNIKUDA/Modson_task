from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/document/{document_id}")
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document_by_id(db, document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document


@app.get("/documents/")
def read_documents(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    db_documents = crud.get_documents(db, skip=skip, limit=limit)
    return db_documents


@app.post("/remove/{document_id}")
def remove_document(document_id: int, db: Session = Depends(get_db)):
    result = crud.remove_document_by_id(db, document_id)
    return result
