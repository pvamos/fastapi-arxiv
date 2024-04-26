# app/write_results/write_results_router.py

from fastapi import APIRouter, HTTPException, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .write_results_functions import write_result_records
from ..dependencies import get_database_session_rw
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to write result data into the database. Accepts JSON data as input and saves it.
@router.post("/write-results", status_code=201)
async def write_results(data: dict = Body(...), db: AsyncSession = Depends(get_database_session_rw)):
    logger.info("write_results(data): len(data)=%d", len(data))
    logger.debug("write_results(data): data=%s", str(data))

    try:
        await write_result_records(db, data)

        return {"message": "Result records saved successfully"}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

