# /app/api/dependencies.py

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi import Depends, HTTPException

engine_rw = create_async_engine(settings.DATABASE_RW_URL, echo=True)
engine_ro = create_async_engine(settings.DATABASE_RO_URL, echo=True)
#engine_sequence = create_async_engine(settings.DATABASE_SEQUENCE_URL, echo=True)

sequence_psycopg2_connect_string = settings.DATABASE_SEQUENCE_STRING

# Sqlalchemy has a known issue with Postgres Sequence objects.
# It is not able perform this simple query:  SELECT nextval('arxiv_sequence');
# So I'm forced to use psycopg2 for this.

SessionLocalRW = sessionmaker(autocommit=False, autoflush=False, bind=engine_rw, class_=AsyncSession)
SessionLocalRO = sessionmaker(autocommit=False, autoflush=False, bind=engine_ro, class_=AsyncSession)
#SessionLocalSEQUENCE = sessionmaker(autocommit=False, autoflush=False, bind=engine_ro, class_=AsyncSession)

default_max_query_results = settings.DEFAULT_MAX_QUERY_RESULTS

results_default_page = int(settings.RESULTS_DEFAULT_PAGE)
results_default_items_per_page = int(settings.RESULTS_DEFAULT_ITEMS_PER_PAGE)

httpx_internal_timeout = int(settings.HTTPX_INTERNAL_TIMEOUT)
httpx_external_timeout = int(settings.HTTPX_EXTERNAL_TIMEOUT)

arxiv_api_url = settings.ARXIV_API_URL
get_sequence_url = settings.GET_SEQUENCE_URL
write_queries_url = settings.WRITE_QUERIES_URL
write_results_url = settings.WRITE_RESULTS_URL
read_queries_url = settings.READ_QUERIES_URL
read_results_url = settings.READ_RESULTS_URL

fastapi_logger_name = settings.FASTAPI_LOGGER_NAME

set_log_level = settings.LOG_LEVEL

# Convert timezone offset parameter to integer, default to 0 if invalid
try:
    timezone_offset = int(settings.TIMEZONE_OFFSET)
except ValueError:
    logger.warn("ValueError converting timezone_offset to int, defaulting to 0. Value: %s ValueError: %s", str(settings.TIMEZONE_OFFSET), str(e))
    timezone_offset = 0


async def get_database_session_rw():
    async_session = SessionLocalRW()
    try:
        yield async_session
    finally:
        await async_session.close()

async def get_database_session_ro():
    async_session = SessionLocalRO()
    try:
        yield async_session
    finally:
        await async_session.close()

#async def get_database_session_sequence():
#    async_session = SessionLocalSEQUENCE()
#    try:
#        yield async_session
#    finally:
#        await async_session.close()