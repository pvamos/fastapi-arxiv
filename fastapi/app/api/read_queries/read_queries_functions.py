# app/read_queries/read_queries_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func, text, expression
from fastapi import HTTPException
from ..models import ArxivQuery
from ..dependencies import timezone_offset
from typing import Optional
import logging



logger = logging.getLogger('fastapi')

async def read_query_data(
    db: AsyncSession,
    start_timestamp: int,
    end_timestamp: Optional[int] = None):
    
    logger.info("read_query_data(start_timestamp=%s, end_timestamp=%s): called", start_timestamp, end_timestamp)

    if start_timestamp is None:
        logger.error("read_query_data(): start_timestamp is 'None', missing compulsory parameter")
        raise HTTPException(status_code=400, detail="read_query_data(): start_timestamp is 'None', missing compulsory parameter.")

    try:
        # Build query conditions
        conditions = [ArxivQuery.timestamp >= start_timestamp]

        if end_timestamp is not None:
            conditions.append(ArxivQuery.timestamp <= end_timestamp)
            logger.debug("read_query_data() end_timestamp=%d is not 'None', adding query criteria):", end_timestamp)
        else:
            logger.debug("read_query_data() end_timestamp is 'None', not adding query criteria")

        # Format the timestamp in the select statement
        formatted_timestamp = func.to_char(func.to_timestamp(ArxivQuery.timestamp + (3600 * timezone_offset)), 'YYYY-MM-DD"T"HH24:MI:SS').label('timestamp')

        # Add "ArXiv Query: " to the beginning of query
        formatted_query = func.concat('ArXiv Query: ', ArxivQuery.query).label('query')

        # Prepare the full query statement
        statement = select(
            formatted_query,
            formatted_timestamp,
            ArxivQuery.status,
            ArxivQuery.num_results
        ).where(*conditions).order_by(ArxivQuery.timestamp.asc())

        logger.debug("read_query_data(): str(statement)=%s", str(statement))

        # Execute the query
        result = await db.execute(statement)

        query_records = result.mappings().all()  # Retrieve results as dictionaries

        logger.debug("read_query_data(start_timestamp=%s, end_timestamp=%s): returning: %s", start_timestamp, end_timestamp, str(query_records))

        return query_records

    except Exception as e:
        logger.error(f"Database query error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
