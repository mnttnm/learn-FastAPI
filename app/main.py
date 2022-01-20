from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm.session import Session
from . import models
from .database import engine, get_db
from .routers import post, user, auth, vote


# create all our models
# you don't need this command as alembic will generate the tables for you now when you will run the migration

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=['*']
)

app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=vote.router)


# This complete definition of path and the function is called as pathoperation.
@app.get("/")
def get_user():
    return {"message": "Welcome"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # db.query essentially just generate the SQL equivalent of the query
    # we are trying to perform.
    posts = db.query(models.Post).all()
    return {"data": posts}
