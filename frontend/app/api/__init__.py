# app/api/__init__.py

from .arxiv import router as arxiv_router
from .queries import router as queries_router
from .results import router as results_router


def init_app(app):
    app.include_router(arxiv_router)
    app.include_router(queries_router)
    app.include_router(results_router)
