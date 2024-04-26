# app/read_results/read_results_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from .read_results_functions import read_results_data
from ..dependencies import get_database_session_ro 
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to fetch result records with pagination from the database.
@router.get("/read-results")
async def read_results(
    page: int = Query(0, description="Page number for pagination"),
    items_per_page: int = Query(10, description="Number of items per page"),
    db: AsyncSession = Depends(get_database_session_ro)):

    logger.debug("read_results(page=%d, items_per_page=%d):", page, items_per_page)

    try: 
        results = await read_results_data(db, page, items_per_page)

        return results

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

