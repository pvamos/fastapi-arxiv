# app/api/queries/queries_functions.py

import httpx
from fastapi import HTTPException
from typing import Optional
from datetime import datetime, timedelta, timezone
import logging
from ..dependencies import httpx_internal_timeout, read_queries_url, fastapi_logger_name

logger = logging.getLogger(fastapi_logger_name)


# Fetch query data from /read-queries endpoint
async def get_query_data(
    start_timestamp: int,
    end_timestamp: Optional[int] = None):
    logger.info("get_query_data(start_timestamp=%s, end_timestamp=%s): called", str(start_timestamp), str(end_timestamp))

    base_url = read_queries_url
    url = f"{base_url}?start_timestamp={start_timestamp}"

    if end_timestamp is not None:
        url += f"&end_timestamp={end_timestamp}"

    try:
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
            
            logger.debug("get_query_data(start_timestamp=%s, end_timestamp=%s): returning: %s", str(start_timestamp), str(end_timestamp), str(response.json()))

            return response.json()

    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch query data")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail="Service to read query data is unavailable")


# Convert date string with timezone offset to datetime object
def convert_to_unix_timestamp(
    date_str: str,
    timezone_offset: Optional[int] = 0):
    logger.info("convert_to_unix_timestamp(date_str=%s, timezone_offset=%s): called", str(date_str), str(timezone_offset))
  
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        # Apply timezone offset
        adjusted_dt = dt - timedelta(hours=timezone_offset)
        unix_timestamp = int(adjusted_dt.replace(tzinfo=timezone.utc).timestamp())

        logger.debug("convert_to_unix_timestamp(date_str=%s, timezone_offset=%s): returning: %s", str(date_str), str(timezone_offset), str(unix_timestamp))

        return unix_timestamp

    except ValueError as e:
        # Handle invalid parameters
        logger.error("convert_to_unix_timestamp(date_str=%s, timezone_offset=%s): ValueError: %s", str(date_str), str(timezone_offset), str(e))
        raise HTTPException(status_code=400, detail=f"convert_to_unix_timestamp(date_str={date_str}, timezone_offset={str(timezone_offset)}): ValueError: {str(e)}")
    except Exception as e:
        logger.error("convert_to_unix_timestamp(date_str=%s, timezone_offset=%s): Unexpected error: %s", str(date_str), str(timezone_offset), str(e))
        raise HTTPException(status_code=400, detail=f"convert_to_unix_timestamp(date_str={date_str}, timezone_offset={str(timezone_offset)}): Exception: {str(e)}")

