from fastapi import FastAPI
from . import models
from .database import engine
from .routers import company, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(company.router)
app.include_router(user.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to api for query reports'}
