# app/read_results/read_results_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import ArxivResult
import logging

logger = logging.getLogger('fastapi')

# Retrieves result records from the database based on pagination.
async def read_results_data(
    db: AsyncSession,
    page: int,
    items_per_page: int):
    logger.info("read_results_data(page=%s, items_per_page=%s): called", str(page), str(items_per_page))
# TypeError: can't multiply sequence by non-int of type 'tuple'
    try: 
        statement = select(
            ArxivResult.author, 
            ArxivResult.title, 
            ArxivResult.journal
        ).offset(page * items_per_page).limit(items_per_page)
        result = await db.execute(statement)

        result_records = result.mappings().all()

        logger.debug("read_results_data(page=%s, items_per_page=%s): returning: %s", str(page), str(items_per_page), str(result_records))

        return result_records

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

