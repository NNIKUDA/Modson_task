import elasticsearch
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import elastic_logic
import crud
import models
from database import SessionLocal, engine
from elastic import elastic_client

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post_by_id(db, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.get("/posts/search/{text}/")
def search_documents(text: str, index_name: str = "posts", db: Session = Depends(get_db), skip: int = 0,
                     limit: int = 20):
    post_ids = elastic_logic.search_posts_by_text(elastic_client, index_name=index_name, text=text, limit=20)
    if not post_ids:
        raise HTTPException(status_code=404, detail=f"Posts not found")
    db_posts = crud.get_posts_by_ids(db, posts_ids=post_ids, skip=skip, limit=limit)
    return db_posts


@app.post("/posts/delete/{post_id}/")
def delete_post(post_id: int, index_name: str = "posts", db: Session = Depends(get_db)):
    try:
        elastic_logic.delete_post_by_id(elastic_client, index_name=index_name, post_id=post_id)
        crud.delete_post_by_id(db, post_id)
    except elasticsearch.NotFoundError as e:
        return {"result": "Error", "detail": "Post not found"}
    return {"result": "Deleted"}
