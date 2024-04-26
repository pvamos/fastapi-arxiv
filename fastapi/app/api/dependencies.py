from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .config import settings
from fastapi import Depends, HTTPException

engine_rw = create_async_engine(settings.DATABASE_RW_URL, echo=True)
engine_ro = create_async_engine(settings.DATABASE_RO_URL, echo=True)
#engine_sequence = create_async_engine(settings.DATABASE_SEQUENCE_URL, echo=True)

sequence_psycopg2_connect_string = settings.DATABASE_SEQUENCE_STRING

# Sqlalchemy has a known issue with Postgres Sequence objects.
# It is not able perform this simple query:  SELECT nextval('arxiv_sequence')
# So I'm forced to use psycopg2 for this.

SessionLocalRW = sessionmaker(autocommit=False, autoflush=False, bind=engine_rw, class_=AsyncSession)
SessionLocalRO = sessionmaker(autocommit=False, autoflush=False, bind=engine_ro, class_=AsyncSession)
#SessionLocalSEQUENCE = sessionmaker(autocommit=False, autoflush=False, bind=engine_ro, class_=AsyncSession)

default_max_query_results = settings.DEFAULT_MAX_QUERY_RESULTS
results_default_page = settings.RESULTS_DEFAULT_PAGE
results_default_items_per_page = settings.RESULTS_DEFAULT_ITEMS_PER_PAGE

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