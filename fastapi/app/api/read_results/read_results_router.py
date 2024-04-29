# app/read_results/read_results_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from .read_results_functions import read_results_data
from ..dependencies import get_database_session_ro
from ..dependencies import results_default_page, results_default_items_per_page
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to fetch result records with pagination from the database.
@router.get("/read-results")
async def read_results(
    db: AsyncSession = Depends(get_database_session_ro),
    page: int = Query(default=results_default_page, description="Page number for pagination"),
    items_per_page: int = Query(default=results_default_items_per_page, description="Number of items per page")):

    logger.notice("read_results(page=%s, items_per_page=%s): called", str(page), str(items_per_page))

    try: 
        results = await read_results_data(db, page, items_per_page)

        logger.info("read_results(page=%s, items_per_page=%s): returning: %s", str(page), str(items_per_page), str(results))

        return results

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

