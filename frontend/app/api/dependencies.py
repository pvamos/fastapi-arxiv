# /app/api/dependencies.py

from .config import settings
from fastapi import Depends, HTTPException


default_max_query_results = settings.DEFAULT_MAX_QUERY_RESULTS

results_default_page = int(settings.RESULTS_DEFAULT_PAGE)
results_default_items_per_page = int(settings.RESULTS_DEFAULT_ITEMS_PER_PAGE)

httpx_internal_timeout = int(settings.HTTPX_INTERNAL_TIMEOUT)

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


