# app/api/get_sequence/get_sequence_router.py

from fastapi import APIRouter, HTTPException
from .get_sequence_functions import retrieve_sequence_value
from ..dependencies import fastapi_logger_name
import logging

logger = logging.getLogger(fastapi_logger_name)


router = APIRouter()

# Endpoint to get a sequence value from the database. This is typically used for generating unique identifiers.
@router.get("/get-sequence")
async def retrieve_sequence():
    logger.notice("retrieve_sequence() called")

    try:
        sequence = await retrieve_sequence_value()

        logger.debug("retrieve_sequence() value is: %s", sequence)

        return {"sequence": sequence}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
