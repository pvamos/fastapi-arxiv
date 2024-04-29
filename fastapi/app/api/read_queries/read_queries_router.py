# app/read_queries/read_queries_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .read_queries_functions import read_query_data
from ..dependencies import get_database_session_ro 
from typing import Optional
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to fetch query records within a specified timestamp range from the database.
@router.get("/read-queries")
async def read_queries(
    start_timestamp: int, 
    end_timestamp: Optional[int] = None, 
    db: AsyncSession = Depends(get_database_session_ro)):

    logger.info("read_queries(start_timestamp=%s, end_timestamp=%s): called", str(start_timestamp), str(end_timestamp))

    try:
    
        queries = await read_query_data(db, start_timestamp, end_timestamp)

        logger.debug("read_queries(start_timestamp=%s, end_timestamp=%s): returning: %s", str(start_timestamp), str(end_timestamp), str(queries))

        return queries

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

