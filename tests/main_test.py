from fastapi import FastAPI
from src.router import prepare_router

app = FastAPI()

prepare_router(app)
