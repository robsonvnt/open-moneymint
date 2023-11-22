from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from investment.interface.portfolio_http import router as portfolio_router
from investment.interface.investment_http import router as investment_router
from investment.interface.consolidated_balance_http import router as consolidated_balance_router
from investment.interface.transaction_http import router as transaction_router
from auth.interface.user_http import router as user_router


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


def prepare_router(app):
    app.add_middleware(NormalizePathMiddleware)

    app.include_router(portfolio_router, prefix="/portfolios")
    app.include_router(investment_router, prefix="/portfolios")
    app.include_router(consolidated_balance_router, prefix="/portfolios")
    app.include_router(transaction_router, prefix="/portfolios")

    app.include_router(user_router, prefix="")
