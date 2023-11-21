from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sentry_sdk

from src.router import prepare_router

sentry_sdk.init(
    dsn="https://da079e56c790d3f9dbe745763e3f73e6@o4506203208744960.ingest.sentry.io/4506203210973184",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

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
    raise Exception("teste")
    return {"status": "ok"}


prepare_router(app)
