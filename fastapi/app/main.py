# app/main.py

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import logging
from .api import init_app
import uvicorn
import os

# Add custom NOTICE logging level
logging.NOTICE = 25
logging.addLevelName(logging.NOTICE, "NOTICE")

# Add custom NOTICE logging level
def notice(self, message, *args, **kws):
    if self.isEnabledFor(logging.NOTICE):
        self._log(logging.NOTICE, message, args, **kws)

# Attaching the custom method to Logger class
logging.Logger.notice = notice

# Configure logging as per your existing setup
def configure_logging():
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()  # Default to INFO if not set
    logging_config = dict(
        version=1,
        disable_existing_loggers=False,
        formatters={
            'detailed': {
                'format': '%(asctime)s [%(levelname)s] %(name)s - %(module)s.%(funcName)s - %(message)s'
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
            'uvicorn': {'handlers': ['console'], 'level': log_level, 'propagate': False},
            'fastapi': {'handlers': ['console'], 'level': log_level, 'propagate': False}
        },
        root={
            'handlers': ['console'],
            'level': log_level,
        },
    )
    logging.config.dictConfig(logging_config)

app = FastAPI()

configure_logging()

logger = logging.getLogger('fastapi')
logger.notice("Logging initialized with %s", os.getenv('LOG_LEVEL', 'INFO').upper())

# Custom exception handler for HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTPException raised: {exc.detail}", exc_info=True)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Setup a general exception handler
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
# (this happens when runing direcly, not in Docker)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
