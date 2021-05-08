from fastapi import FastAPI
from typing import Optional
# use pydantic to creta BaseModel
from pydantic import BaseModel
app = FastAPI()

# @app is decoration of operation
# get is operation of path
# ('/') is path of opration
# Query parameters
@app.get('/blog')
# this is path operation function
# accepted parameter limit
# initial the parameters as default value when you access just a /blog path
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # check data type with return published
    if published:
        return {'data':f'{limit} published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}

# fast api read the file line by line
# this same like '/blog/{id}'
@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blog'}


# use parantasies calibrases{} to fetch
@app.get('/blog/{id}')
# accepted variable in function with str type default
# define id as int example: id: int
def show(id: int):
    # fetch blog with id = id
    return {'data':id}


@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of blog with id = id
    return {'data': {'1','2'}}


# create some class model for try post Request
class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
# accept parameters from BaseModel blog
def create_blog(blog: Blog):
    # access the title to get value of request body blogs
    return {'data': f"Blog is created with title as {blog.title}"}
