# app/read_results/read_results_functions.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from ..models import ArxivResult
import logging

logger = logging.getLogger('fastapi')

# Retrieves result records from the database based on pagination.
async def read_results_data(db: AsyncSession, page: int, items_per_page: int):
    logger.debug("read_results_data(page=%d, items_per_page=%d):", page, items_per_page)

    try: 
        statement = select(ArxivResult).offset(page * items_per_page).limit(items_per_page)
        result = await db.execute(statement)
        result_records = result.scalars().all()

        return result_records

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query error: {str(e)}")

