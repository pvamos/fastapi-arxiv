# app/api/config.py

import os

class Settings:
    DATABASE_RW_URL: str = os.getenv("DATABASE_RW_URL")
    DATABASE_RO_URL: str = os.getenv("DATABASE_RO_URL")
    # DATABASE_SEQUENCE_URL: str = os.getenv("DATABASE_SEQUENCE_URL")
    # Sqlalchemy has a known issue with Postgres Sequence objects.
    # It is not able perform this simple query:  SELECT nextval('arxiv_sequence')
    # So I'm forced to use psycopg2 for this.
    DATABASE_SEQUENCE_STRING: str = os.getenv("DATABASE_SEQUENCE_STRING")
    DEFAULT_MAX_QUERY_RESULTS: int = os.getenv("DEFAULT_MAX_QUERY_RESULTS")
    RESULTS_DEFAULT_PAGE=os.getenv("RESULTS_DEFAULT_PAGE")
    RESULTS_DEFAULT_ITEMS_PER_PAGE=os.getenv("RESULTS_DEFAULT_ITEMS_PER_PAGE")
    TIMEZONE_OFFSET=os.getenv("TIMEZONE_OFFSET")
    HTTPX_INTERNAL_TIMEOUT=os.getenv("HTTPX_INTERNAL_TIMEOUT")
    HTTPX_EXTERNAL_TIMEOUT=os.getenv("HTTPX_EXTERNAL_TIMEOUT")
    LOG_LEVEL=os.getenv("LOG_LEVEL")

settings = Settings()
