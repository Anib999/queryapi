from fastapi import FastAPI
from . import models
from .database import engine
from .routers import company, user, auth, comment, folder, query, like


models.Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})


app.include_router(company.router)
app.include_router(folder.router)
app.include_router(query.router)
app.include_router(user.router)
app.include_router(comment.router)
app.include_router(like.router)
app.include_router(auth.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to api for query reports'}
