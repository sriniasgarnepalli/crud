from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, users, auth, vote
from .config import settings

# commented the below line after using alembic for versioning of postgres tables
# The below line is used to check in models table to create a table if it is not exists previoulsy on every restart.
# models.Base.metadata.create_all(bind=engine)

origins = ["https://www.google.com","https://twitter.com","https://fastapi.tiangolo.com"]

# If you need to setup a public api for everyone to access if use prigins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"sri":"Hey this is Srinivas"}