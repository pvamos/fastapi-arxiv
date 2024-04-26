from .arxiv import router as arxiv_router
from .arxiv_api import router as arxiv_api_router
from .get_sequence import router as get_sequence_router
from .queries import router as queries_router
from .read_queries import router as read_queries
from .read_results import router as read_results_router
from .results import router as results_router
from .write_queries import router as write_queries_router
from .write_results import router as write_results_router


def init_app(app):
    app.include_router(arxiv_router)
    app.include_router(arxiv_api_router)
    app.include_router(get_sequence_router)
    app.include_router(queries_router)
    app.include_router(read_queries)
    app.include_router(read_results_router)
    app.include_router(results_router)
    app.include_router(write_queries_router)
    app.include_router(write_results_router)
