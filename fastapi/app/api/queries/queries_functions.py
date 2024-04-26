# app/queries/queries_functions.py

import httpx
from fastapi import HTTPException
from typing import Optional
import logging

logger = logging.getLogger('fastapi')


# Fetches query data from the /read-queries endpoint.
async def get_query_data(start_timestamp: int, end_timestamp: Optional[int] = None):
    logger.debug("get_query_data(start_timestamp=%s, end_timestamp=%s):", str(start_timestamp), str(end_timestamp))

    url = f"http://localhost:8000/read-queries?start_timestamp={start_timestamp}"
    if end_timestamp is not None:
        url += f"&end_timestamp={end_timestamp}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()

            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch query data")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Service to read query data is unavailable")

