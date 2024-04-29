# app/queries/queries_router.py

from fastapi import APIRouter, Depends, HTTPException, Query, Response, Body
from .queries_functions import get_query_data, convert_to_unix_timestamp
from typing import Optional
from ..dependencies import timezone_offset
import json
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()

# Endpoint to fetch query data through the /read-queries internal API call and return as a file.
@router.get("/queries")
async def queries_get(
    start_timestamp: str = Query(None, description="Start timestamp for query retrieval"),
    end_timestamp: Optional[str] = Query(None, description="End timestamp for query retrieval")):

    logger.notice("queries_get(start_timestamp=%s, end_timestamp=%s): called", start_timestamp, end_timestamp)

    if start_timestamp is None:
        raise HTTPException(status_code=400, detail="queries_get(): Required parameter missing: start_timestamp")    

    start_timestamp_unix = convert_to_unix_timestamp(start_timestamp, timezone_offset)

    end_timestamp_unix = None

    # If end_timestamp is None, end_timestamp_unix stays None
    if end_timestamp is not None:
            end_timestamp_unix = convert_to_unix_timestamp(end_timestamp, timezone_offset)

    try:
        query_data = await get_query_data(start_timestamp_unix, end_timestamp_unix)
        json_compatible_data = json.dumps(query_data)

        response = Response(content=json_compatible_data, media_type="application/json", headers={"Content-Disposition": "attachment; filename=query_data.json"})

        logger.debug("queries_get(start_timestamp=%s, end_timestamp=%s): returning: %s", start_timestamp, end_timestamp, str(response))

        return response

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


# Endpoint to fetch query data through the /read-queries internal API call and return as a JSON object.
@router.post("/queries")
async def queries_post(
    start_timestamp: str = Body(None, embed=True, description="Start timestamp for query retrieval"),
    end_timestamp: Optional[str] = Body(None, embed=True, description="End timestamp for query retrieval")):

    logger.notice("queries_get(start_timestamp=%s, end_timestamp=%s): called", start_timestamp, end_timestamp)

    if start_timestamp is None:
        raise HTTPException(status_code=400, detail="queries_get(): Required parameter missing: start_timestamp")    

    start_timestamp_unix = convert_to_unix_timestamp(start_timestamp, timezone_offset)

    if start_timestamp_unix is None:
        raise HTTPException(status_code=400, detail="queries_get(): Required parameter is None start_timestamp_unix")

    end_timestamp_unix = None
    
    # If end_timestamp is None, end_timestamp_unix stays None
    if end_timestamp is not None:
            end_timestamp_unix = convert_to_unix_timestamp(end_timestamp, timezone_offset)
    try:
        query_data = await get_query_data(start_timestamp_unix, end_timestamp_unix)

        logger.debug("queries_post(start_timestamp=%s, end_timestamp=%s): returning: %s", str(start_timestamp), str(end_timestamp), str(query_data))

        return query_data

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

