# app/read_queries/read_queries_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import ArxivQuery
from typing import Optional
import logging

logger = logging.getLogger('fastapi')


# Retrieves query records from the database within the specified timestamp range.
async def read_query_data(db: AsyncSession, start_timestamp: int, end_timestamp: Optional[int] = None):
    logger.info("read_query_data(start_timestamp=%s, end_timestamp=%s):", start_timestamp, end_timestamp)

    try:
        # Check start_timestamp parameter
        if start_timestamp is None:
            logger.debug("read_query_data() start_timestamp is 'None', missing complusory parameter")
            raise HTTPException(status_code=400, detail=f"read_query_data(): start_timestamp is 'None', missing complusory parameter.")
        else:
            logger.debug("read_query_data() start_timestamp is not 'None', complusory parameter present: start_timestamp=%d" , start_timestamp)

        # Start building the query conditions
        conditions = [ArxivQuery.timestamp >= start_timestamp]

        # Add condition for end_timestamp if it is not None
        if end_timestamp is not None:
            conditions.append(ArxivQuery.timestamp <= end_timestamp)
            logger.debug("read_query_data() end_timestamp=%d is not 'None', adding query criteria):", end_timestamp)
        else:
            logger.debug("read_query_data() end_timestamp is 'None', not adding query criteria")

        # Prepare the full query statement
        statement = select(ArxivQuery).where(
            *conditions  # Unpack conditions list into where clause
        ).order_by(ArxivQuery.timestamp.asc())

        logger.debug("read_query_data(): str(statement)=%s", str(statement))

        # Execute the query
        result = await db.execute(statement)
        query_records = result.scalars().all()

        return query_records

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")
