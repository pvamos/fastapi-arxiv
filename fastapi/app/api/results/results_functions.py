# app/results/results_functions.py

import httpx
from fastapi import HTTPException
import logging
from ..dependencies import httpx_internal_timeout

logger = logging.getLogger('fastapi')


# Fetches result data from the /read-results endpoint.
async def get_results_data(page: int, items_per_page: int):
    logger.info("get_results_data(page=%s, items_per_page=%s): called", str(page), str(items_per_page))

    url = f"http://localhost:8000/read-results?page={page}&items_per_page={items_per_page}"
    try:
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            logger.info("get_results_data(page=%s, items_per_page=%s): returning: %s", str(page), str(items_per_page), str(response.json()))
            
            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch result data")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Service to read result data is unavailable")

