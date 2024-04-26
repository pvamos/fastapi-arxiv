# app/write_results/write_results_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from ..models import ArxivResult
import logging

logger = logging.getLogger('fastapi')


# Saves result records in the database.
async def write_result_records(db: AsyncSession, result_data: dict):
    logger.info("write_result_records(result_data): len(query_data)=%d", len(result_data))
    logger.debug("write_result_records(result_data): query_data=%s", str(result_data))

    try:
        # Add an incremental result_number=index to each result
        new_results = [
            ArxivResult(
                query_id=result_data.get('query_id'),
                timestamp=result_data.get('timestamp'),
                result_number=index,
                author=result.get('authors', None),
                title=result.get('title', None),
                journal=result.get('journal', None)
            )
            for index, result in enumerate(result_data['results'])
        ]
        db.add_all(new_results)
        await db.commit()

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save result records: {str(e)}")

