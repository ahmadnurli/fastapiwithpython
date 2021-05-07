from fastapi import FastAPI

app = FastAPI()

# @app is decoration of operation
# get is operation of path
# ('/') is path of opration
@app.get('/')
# this is path operation function
def index():
    return {'data':{'name': 'nurli'}}


@app.get('/about')
def about():
    return {'data':'about page'}
