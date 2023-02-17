from sqlalchemy.orm import Session
import models


def get_posts_by_ids(db: Session, posts_ids: list, skip: int = 0, limit: int = 20):
    return db.query(models.Post).filter(models.Post.id.in_(posts_ids)).order_by(models.Post.created_date).offset(skip).limit(20).all()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def delete_post_by_id(db: Session, post_id: int):
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    return db.commit()


