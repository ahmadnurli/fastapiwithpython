from os import stat
from fastapi import FastAPI, status, Response, HTTPException
from fastapi.params import Depends
from . import models, schemas
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

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


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id ==
                                        id).delete(synchronize_session=False)
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'message': f'Blog with the id {id} id not available'}

    db.commit()
    return {'message': 'Delete is successfully'}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(
        models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} is not found")

    blog.update(request)
    db.commit()
    return 'updated'


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


# if __name__ == '__main__':
#     uvicorn.run(app, host="127.0.0.1", port=9000)
