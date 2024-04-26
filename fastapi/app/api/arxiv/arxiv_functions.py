# app/arxiv/arxiv_functions.py

import httpx
from fastapi import HTTPException
import feedparser
import logging

logger = logging.getLogger('fastapi')


# Build query search parameters for /arxiv-api endpoint
def build_query_params(author, title, journal, max_results):
    logger.debug("build_query_params(author=%s, title=%s, journal=%s, max_results=%s):", author, title, journal, max_results)

    query_params = {}
    if author:
        query_params['author'] = author
    if title:
        query_params['title'] = title
    if journal:
        query_params['journal'] = journal
    query_params['max_results'] = max_results

    return query_params


# Interacts with the /arxiv-api endpoint to fetch data and handle errors appropriately.
async def fetch_arxiv_data(author, title, journal, max_results):
    logger.debug("fetch_arxiv_data(author=%s, title=%s, journal=%s, max_results=%s)", author, title, journal, max_results)

    base_url = "http://localhost:8000/arxiv-api"
    query_params = build_query_params(author, title, journal, max_results)
    query_string = "&".join(f"{key}={value}" for key, value in query_params.items() if value is not None)
    api_url = f"{base_url}?{query_string}"

    try:
        async with httpx.AsyncClient() as client:
            logger.debug("fetch_arxiv_data(): /arxiv-api URL: %s", api_url)

            response = await client.get(api_url)
            response.raise_for_status()

            logger.debug("fetch_arxiv_data(): Fetched from arXiv API: %s", str(response.text))

            return response.json()['data'], response.json()['timestamp'], response.json()['status'], response.json()['num_results'], response.json()['num_entries'], response.json()['query']

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when fetching data: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Error fetching data from internal arXiv API endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when calling arXiv API: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Internal arXiv API service is unavailable: {str(e)}")


# Processes the feed data parsed by feedparser and structures it for response.
def process_feed(feed):
    logger.info("process_feed(feed): len(feed)=%d", len(feed))
    logger.debug("process_feed(feed): feed=%s", str(feed))

    results = []
    for entry in feed.entries:
        result = {
            "authors": [author.name for author in entry.authors if hasattr(entry, 'authors')],
            "title": entry.title,
            "journal": getattr(entry, 'journal', '')
        }
        results.append(result)

    logger.debug("process_feed(): value=%s", str(results))

    return results


# Fetches a unique postgres sequence value from the /get-sequence endpoint.
async def get_sequence_value():
    logger.debug("get_sequence_value()")
    
    api_url = "http://localhost:8000/get-sequence"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            response.raise_for_status()
            logger.debug("Sequence value retrieved: %s", response.json()['sequence'])

            return response.json()['sequence']

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when fetching sequence value: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to get sequence value from internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when fetching sequence value: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to get sequence data is unavailable: {str(e)}")


# Saves a record to 'queries' table using the /write-queries endpoint.
async def save_query_record(query_id, timestamp, status, num_results, num_entries, query):
    logger.info("save_query_record(): query_id=%d, timestamp=%d, status=%d, num_results=%d, num_entries=%d, query=%s", query_id, timestamp, status, num_results, num_entries, query)

    api_url = "http://localhost:8000/write-queries"
    query_data = {
        "query_id": query_id,
        "timestamp": timestamp,
        "status": status,
        "num_results": num_results,
        "num_entries": num_entries,
        "query": query
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=query_data)
            response.raise_for_status()
            logger.info("save_query_record(): Record with ID %d inserted to 'queries' table", query_id)
            logger.info("save_query_record(): Record successfully inserted to 'quesries table': %s", str(query_data))

            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when saving query record: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to save query record via internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when saving query record: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to write query data is unavailable: {str(e)}")


# Saves result records to 'results' table using the /write-results endpoint.
async def save_result_records(query_id, timestamp, results):
    logger.debug("save_result_records(query_id, results): query_id=%d, len(results)=%d", query_id, len(results))

    api_url = "http://localhost:8000/write-results"
    results_data = {
        "query_id": query_id,
        "timestamp": timestamp,
        "results": results
    }

    try: 
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, json=results_data)
            response.raise_for_status()
            logger.info("save_result_record(): Records with ID %s inserted to 'records' table" , query_id)
            logger.debug("save_query_record(): : %s", str(results))

            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error("HTTP status error when saving result records: %s", str(e))
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to save result records via internal endpoint: {str(e)}")
    except httpx.RequestError as e:
        logger.error("Request error when saving result records: %s", str(e))
        raise HTTPException(status_code=503, detail=f"Service to write result data is unavailable: {str(e)}")
