# app/write_queries/write_queries_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ..models import ArxivQuery
import logging

logger = logging.getLogger('fastapi')


# Saves a query record in the database.
async def write_query_record(db: AsyncSession, query_data: dict):
    logger.info("write_query_record(query_data): len(query_data)=%d", len(query_data))
    logger.debug("write_query_record(query_data): query_data=%s", str(query_data))

    try:
        new_query = ArxivQuery(
            query_id=query_data.get('query_id'),
            timestamp=query_data.get('timestamp'),
            status=query_data.get('status'),
            num_results=query_data.get('num_results'),
            num_entries=query_data.get('num_entries'),
            query=query_data.get('query')
        )

        db.add(new_query)
        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save query record: {str(e)}")
