# app/results/results_router.py

from fastapi import APIRouter, Depends, HTTPException, Query
from .results_functions import get_results_data
from typing import Optional
from ..dependencies import results_default_page, results_default_items_per_page
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Endpoint to fetch result data through the /read-results internal API call.
@router.get("/results")
async def results(
    page: Optional[int] = Query(results_default_page, description="Page number for pagination"),
    items_per_page: Optional[int] = Query(results_default_items_per_page, description="Number of items per page")):

    logger.debug("results(page=%d, items_per_page=%d):", page, items_per_page)

    try:
        result_data = await get_results_data(page, items_per_page)

        return result_data

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

