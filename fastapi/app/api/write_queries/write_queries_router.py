# app/write_queries/write_queries_router.py

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from .write_queries_functions import write_query_record
from ..dependencies import get_database_session_rw
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to write a query record into the database. Accepts JSON data as input and saves it.
@router.post("/write-queries", status_code=201)
async def write_query(data: dict = Body(...), db: AsyncSession = Depends(get_database_session_rw)):
    logger.notice("write_query(data): len(data)=%d", len(data))
    logger.debug("write_query(data): data=%s", str(data))

    try:
        await write_query_record(db, data)

        return {"message": "Query record saved successfully"}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

