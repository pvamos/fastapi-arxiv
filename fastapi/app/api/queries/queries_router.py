# app/queries/queries_router.py

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from .queries_functions import get_query_data
from typing import Optional
import json
import logging

logger = logging.getLogger('fastapi')


router = APIRouter()

# Endpoint to fetch query data through the /read-queries internal API call and return as a file.
@router.get("/queries")
async def queries_get(
    start_timestamp: int = Query(None, description="Start timestamp for query retrieval"),
    end_timestamp: Optional[int] = Query(None, description="End timestamp for query retrieval")):

    logger.debug("queries_get(start_timestamp=%s, end_timestamp=%s):", str(start_timestamp), str(end_timestamp))

    if start_timestamp is None:
        raise HTTPException(status_code=400, detail="queries_get(): Required parameter missing: start_timestamp")

    try:
        query_data = await get_query_data(start_timestamp, end_timestamp)
        json_compatible_data = json.dumps(query_data)

        return Response(content=json_compatible_data, media_type="application/json", headers={"Content-Disposition": "attachment; filename=query_data.json"})

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)


# Endpoint to fetch query data through the /read-queries internal API call and return as a JSON object.
@router.post("/queries")
async def queries_post(
    start_timestamp: int = Query(None, description="Start timestamp for query retrieval"),
    end_timestamp: Optional[int] = Query(None, description="End timestamp for query retrieval")):
    
    logger.debug("queries_post(start_timestamp=%s, end_timestamp=%s):", str(start_timestamp), str(end_timestamp))

    if start_timestamp is None or end_timestamp is None:
        raise HTTPException(status_code=400, detail="Both start and end timestamps are required")
    try:
        query_data = await get_query_data(start_timestamp, end_timestamp)

        return query_data

    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

