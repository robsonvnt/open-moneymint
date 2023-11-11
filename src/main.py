from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
import sentry_sdk

from src.investment.interface.portfolio_http import router as portfolio_router
from src.investment.interface.investment_http import router as investment_router
from src.investment.interface.consolidated_balance_http import router as consolidated_balance_router

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


class NormalizePathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        path = request.url.path
        if path != '/' and path.endswith('/'):
            # Remover a barra final para rotas não raiz
            path = path.rstrip('/')
            # Atualizar o caminho no escopo da solicitação
            scope = request.scope
            scope['path'] = path
            # Criar uma nova Request com o escopo modificado
            request = Request(scope)
        response = await call_next(request)
        return response


app.add_middleware(NormalizePathMiddleware)

app.include_router(portfolio_router, prefix="/portfolios")
app.include_router(investment_router, prefix="/portfolios")
app.include_router(consolidated_balance_router, prefix="/portfolios")

# Resolve o problema de terminar com / ou não dos paths
