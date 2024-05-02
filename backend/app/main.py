# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
import uvicorn
import os
from .api.dependencies import set_log_level, fastapi_logger_name
from .api import init_app


# Add custom NOTICE logging level
logging.NOTICE = 25
logging.addLevelName(logging.NOTICE, "NOTICE")


# Custom NOTICE logging method with stacklevel adjustment
def notice(self, message, *args, **kws):
    if self.isEnabledFor(logging.NOTICE):
        # stacklevel=2 ensures the correct function call location is logged
        self._log(logging.NOTICE, message, args, kws, stacklevel=2)


# Attaching the custom method to Logger class
logging.Logger.notice = notice


# Function to initialize logging
def configure_logging():
    log_level = set_log_level.upper()
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'detailed': {
                'format': '%(asctime)s %(levelname)s %(name)s - %(module)s.%(funcName)s - %(message)s'
            }
        },
        handlers={
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'detailed',
                'level': log_level
            }
        },
        loggers={
            fastapi_logger_name: {'handlers': ['console'], 'level': log_level, 'propagate': False},
            'httpcore':          {'handlers': ['console'], 'level': log_level, 'propagate': False},
            'httpx':             {'handlers': ['console'], 'level': log_level, 'propagate': False},
            'sqlalchemy':        {'handlers': ['console'], 'level': log_level, 'propagate': False},
            'uvicorn':           {'handlers': ['console'], 'level': log_level, 'propagate': False}
        },
        root={
            'handlers': ['console'],
            'level': log_level,
        },
    )
    logging.config.dictConfig(logging_config)


app = FastAPI()


configure_logging()


logger = logging.getLogger(fastapi_logger_name)
logger.notice("Logging initialized with %s", os.getenv('LOG_LEVEL', 'INFO').upper())


# HTTPException handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException raised: {exc.detail}", exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


# General exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred", exc_info=True)  # Log the traceback
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred"}
    )


# Include routers and other configurations
init_app(app)


# This only runs if main.py is called directly, and not imported
#  (happens when running directly, not in Docker)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
