# app/api/arxiv/arxiv_functions.py

import httpx
from fastapi import HTTPException
import feedparser
import logging
from ..dependencies import httpx_internal_timeout, arxiv_api_url, get_sequence_url, write_queries_url, write_results_url, fastapi_logger_name

logger = logging.getLogger(fastapi_logger_name)


# Build /arxiv-api endpoint search parameters
def build_query_params(
    author,
    title,
    journal,
    max_results):
    logger.info("build_query_params(author=%s, title=%s, journal=%s, max_results=%s): called", author, title, journal, max_results)

    query_params = {}
    if author:
        query_params['author'] = author
    if title:
        query_params['title'] = title
    if journal:
        query_params['journal'] = journal
    query_params['max_results'] = max_results

    logger.debug("build_query_params(author=%s, title=%s, journal=%s, max_results=%s): returning: %s", author, title, journal, max_results, str(query_params))
    
    return query_params


# Fetch data from /arxiv-api endpoint
async def fetch_arxiv_data(
    author,
    title,
    journal,
    max_results):
    logger.info("fetch_arxiv_data(author=%s, title=%s, journal=%s, max_results=%s): called", author, title, journal, max_results)

    base_url = arxiv_api_url
    query_params = build_query_params(author, title, journal, max_results)
    query_string = "&".join(f"{key}={value}" for key, value in query_params.items() if value is not None)
    api_url = f"{base_url}?{query_string}"

    try:
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            logger.debug("fetch_arxiv_data(): /arxiv-api URL: %s", api_url)

            response = await client.get(api_url)
            response.raise_for_status()

            logger.debug("fetch_arxiv_data(author=%s, title=%s, journal=%s, max_results=%s): returning: str(response.text)=%s", author, title, str(journal), max_results, str(response.text))

            return response.json()['data'], response.json()['timestamp'], response.json()['status'], response.json()['num_results'], response.json()['num_entries'], response.json()['query']

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when fetching data: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching data from internal arXiv API endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when calling arXiv API: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Internal arXiv API service is unavailable: {str(e)}")


# Process feed data, transform 'authors'
def process_feed(feed):
    logger.info("process_feed(feed): called: len(feed)=%d", len(feed))
    logger.debug("process_feed(feed): called: feed=%s", str(feed))

    results = []
    for entry in feed.entries:
        result = {
            "authors": [author.name for author in entry.authors if hasattr(entry, 'authors')],
            "title": entry.title,
            "journal": getattr(entry, 'journal', '')
        }
        results.append(result)

    logger.debug("process_feed(%s): returning: %s", str(feed), str(results))

    return results


# Fetch a unique postgres sequence value from /get-sequence endpoint
async def get_sequence_value():
    logger.info("get_sequence_value(): called")
    
    api_url = get_sequence_url

    try:
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            response = await client.get(api_url)
            response.raise_for_status()
            logger.debug("get_sequence_value(): returning: %s", response.json()['sequence'])

            return response.json()['sequence']

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when fetching sequence value: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to get sequence value from internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when fetching sequence value: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to get sequence data is unavailable: {str(e)}")


# Save a record to 'queries' table using /write-queries endpoint
async def save_query_record(
    query_id,
    timestamp,
    status,
    num_results,
    num_entries,
    query):
    logger.info("save_query_record(query_id=%d, timestamp=%d, status=%d, num_results=%d, num_entries=%d, query=%s): called", query_id, timestamp, status, num_results, num_entries, query)

    api_url = write_queries_url
    query_data = {
        "query_id": query_id,
        "timestamp": timestamp,
        "status": status,
        "num_results": num_results,
        "num_entries": num_entries,
        "query": query
    }
    try:
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            response = await client.post(api_url, json=query_data)
            response.raise_for_status()
            logger.debug("save_query_record(uery_id=%d, timestamp=%d, status=%d, num_results=%d, num_entries=%d, query=%s): Record with ID %d inserted to 'queries' table. Record: %s, str(response)=%s", query_id, timestamp, status, num_results, num_entries, query, query_id, str(query_data), str(response))

            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when saving query record: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to save query record via internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when saving query record: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to write query data is unavailable: {str(e)}")


# Save result records to 'results' table using the /write-results endpoint
async def save_result_records(query_id, timestamp, results):
    logger.info("save_result_records(query_id=%s, timestamp=%s, results): called: len(results)=%d", str(query_id), str(timestamp), len(results))
    logger.debug("save_result_records(query_id=%s, timestamp=%s, results): called: str(results)=%s", str(query_id), str(timestamp), str(results))


    api_url = write_results_url
    results_data = {
        "query_id": query_id,
        "timestamp": timestamp,
        "results": results
    }

    try: 
        async with httpx.AsyncClient(timeout=httpx_internal_timeout) as client:
            response = await client.post(api_url, json=results_data)
            response.raise_for_status()
            logger.debug("save_result_records(query_id=%s, timestamp=%s, str(results)=%s): Records inserted to 'queries' table. str(response)=%s", str(query_id), str(timestamp), str(results), str(response))

            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when saving result records: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to save result records via internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when saving result records: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to write result data is unavailable: {str(e)}")
