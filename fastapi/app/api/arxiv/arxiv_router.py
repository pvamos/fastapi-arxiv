# app/api/arxiv/arxiv_router.py

from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from .arxiv_functions import fetch_arxiv_data, get_sequence_value, save_query_record, save_result_records
from ..dependencies import default_max_query_results
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()


# Fetches data from the arXiv API based on the given parameters
# and stores it to 'queries' and 'results' DB tables.
# Sends response:
# {"timestamp": Unix timestamp, "status": HTTP status, "num_results": number of results repored by arXiv API}
@router.get("/arxiv")
async def search_arxiv(
    author: Optional[str] = Query(None, min_length=1, description="Author's name to filter"),
    title: Optional[str] = Query(None, min_length=1, description="Title to filter"),
    journal: Optional[str] = Query(None, min_length=1, description="Journal name to filter"),
    max_results: Optional[int] = Query(default_max_query_results, ge=1, description="Maximum number of results to return")):

    logger.notice("search_arxiv(author=%s, title=%s, journal=%s, max_results=%d): called", author, title, journal, max_results)

    if not (author or title or journal):
        logger.error("search_arxiv(): Validation failed: At least one search parameter must be provided")
        raise HTTPException(status_code=400, detail="At least one search parameter must be provided")

    try:

        data, timestamp, status, num_results, num_entries, query = await fetch_arxiv_data(author, title, journal, max_results)

        query_id = await get_sequence_value()

        await save_query_record(query_id, timestamp, status, num_results, num_entries, query)
        await save_result_records(query_id, timestamp, data)

        logger.debug("search_arxiv(author=%s, title=%s, journal=%s, max_results=%d): Successfully processed query with ID %d, returns: %s", author, title, journal, max_results, query_id, str({"timestamp": timestamp, "status": status, "num_results": num_results, "num_entries": num_entries}))

        return {"timestamp": timestamp, "status": status, "num_results": num_results, "num_entries": num_entries}

    except HTTPException as e:
        logger.error("HTTPException occurred: %s", str(e))
        raise
    except Exception as e:
        logger.exception("Unexpected error occurred: %s", str(e))
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


