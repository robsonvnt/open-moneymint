from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from router import prepare_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos
    allow_headers=["*"],  # Permite todos os cabeçalhos
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


prepare_router(app)
