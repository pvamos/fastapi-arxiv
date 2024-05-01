# app/api/arxiv_api/arxiv_api_router.py

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from .arxiv_api_functions import scrape_arxiv_api, process_feed
import logging
from ..dependencies import default_max_query_results

logger = logging.getLogger('fastapi')


router = APIRouter()


# Fetches data from the arXiv API based on the given parameters and returns the data
# along with the HTTP status code and timestamp from the returned Date header of the arXiv API request.
@router.get("/arxiv-api")
async def search_arxiv_api(
    author: Optional[str] = Query(None, min_length=1, description="Author's name to filter"),
    title: Optional[str] = Query(None, min_length=1, description="Title to filter"),
    journal: Optional[str] = Query(None, min_length=1, description="Journal name to filter"),
    max_results: Optional[int] = Query(default_max_query_results, ge=1, description="Maximum number of results to return")):

    logger.notice("search_arxiv_api(author=%s, title=%s, journal=%s, max_results=%s): called", author, title, journal, str(max_results))

    try:
        feed, timestamp, status, num_results, num_entries, query = await scrape_arxiv_api(author, title, journal, max_results)
        results = process_feed(feed)

        logger.debug("search_arxiv_api(author=%s, title=%s, journal=%s, max_results=%s): returning: %s", author, title, journal, str(max_results), str({"data": results, "timestamp": timestamp, "status": status, "num_results": num_results, "num_entries": num_entries, "query": query}))

        return {"data": results, "timestamp": timestamp, "status": status, "num_results": num_results, "num_entries": num_entries, "query": query}

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


 
