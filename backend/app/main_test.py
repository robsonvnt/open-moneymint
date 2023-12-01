from fastapi import FastAPI

from router import prepare_router

app = FastAPI()

prepare_router(app)
