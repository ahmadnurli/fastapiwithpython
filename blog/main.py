from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from starlette.status import HTTP_404_NOT_FOUND
from . import schemas, models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

import blog

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_200_OK)
def destroy(id, response: Response, db: Session = Depends(get_db)):

    blog = db.query(models.Blog).filter(models.Blog.id ==
                                        id).delete(synchronize_session=False)
    if blog:
        db.commit()
        return {'detail': 'Delete is successfully'}
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with the id {id} id not available'}


@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id', status_code=status.HTTP_200_OK)
def show(id,  response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Blog with the id {id} id not available')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f'Blog with the id {id} id not available'}
    return blog
