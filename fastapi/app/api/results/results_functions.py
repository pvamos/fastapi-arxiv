# app/results/results_functions.py

import httpx
from fastapi import HTTPException
import logging

logger = logging.getLogger('fastapi')


# Fetches result data from the /read-results endpoint.
async def get_results_data(page: int, items_per_page: int):
    logger.debug("get_results_data(page=%d, items_per_page=%d):", page, items_per_page)

    url = f"http://localhost:8000/read-results?page={page}&items_per_page={items_per_page}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch result data")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Service to read result data is unavailable")

