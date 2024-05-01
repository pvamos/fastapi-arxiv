# app/api/schemas.py

from pydantic import BaseModel

class QueryRange(BaseModel):
    query_timestamp_start: int
    query_timestamp_end: int = None

