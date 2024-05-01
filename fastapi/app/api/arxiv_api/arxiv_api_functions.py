# app/api/arxiv_api/arxiv_api_functions.py

import httpx
from fastapi import HTTPException
import feedparser
from email.utils import parsedate_to_datetime
import logging
from ..dependencies import httpx_external_timeout

logger = logging.getLogger('fastapi')


# Constructs the search query for the arXiv API.
def build_search_query(author: str = None, title: str = None, journal: str = None):
    logger.info("build_search_query(author=%s, title=%s, journal=%s): called", author, title, journal)

    search_query_parts = []

    try:
        if author:
            search_query_parts.append(f"au:{author}")
        if title:
            search_query_parts.append(f"ti:{title}")
        if journal:
            search_query_parts.append(f"jr:{journal}")
    
        if not search_query_parts:
            logging.error("HTTP 400 At least one search parameter must be provided: %s", str(e))
            raise HTTPException(status_code=400, detail="At least one search parameter must be provided.")

    except Exception as e:
        logging.error("Parameter validation error: %s", str(e))
        raise HTTPException(status_code=422, detail=f"Invalid search parameters: {str(e)}")

    retval = '+AND+'.join(search_query_parts)
    logger.debug("build_search_query(author=%s, title=%s, journal=%s): returning: %s", author, title, journal, str(retval))


    return retval


# Fetches data from the external arXiv API and handles HTTP errors.
async def scrape_arxiv_api(author, title, journal, max_results):
    logger.info("scrape_arxiv_api(author=%s, title=%s, journal=%s, max_results=%s): called", author, title, journal, max_results)

    search_query = build_search_query(author, title, journal)
    url = f"https://export.arxiv.org/api/query?search_query={search_query}&max_results={max_results}"

    try:
        async with httpx.AsyncClient(timeout=httpx_external_timeout) as client:
            logger.info("httpx.client.get(%s)", url)
            response = await client.get(url)
            response.raise_for_status()
            logger.info("httpx.client.get(%s): HTTP %d", url, response.status_code)
    
            feed = feedparser.parse(response.content)
            logger.debug("scrape_arxiv_api() str(feed)=%s", str(feed))
            
            if not feed.entries:
                logging.error("scrape_arxiv_api(): HTTP 404, No results found.")
                raise HTTPException(status_code=404, detail=f"scrape_arxiv_api(): No results found. {str(e)}")

            # Get Unix timestamp from the Date header in the response
            timestamp = parsedate_to_datetime(response.headers['Date']).timestamp()
            total_results = int(feed.feed.get("opensearch_totalresults", "0"))
            num_entries = len(feed.entries)
            query_title = feed.feed.get("title", "").split(": ", 1)[-1]


    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Failed to fetch data from arXiv API: {str(e)}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"arXiv API service is unavailable: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing arXiv API response: {str(e)}")

    logger.debug("scrape_arxiv_api(author=%s, title=%s, journal=%s, max_results=%s): returning: feed=%s, timestamp=%s, response.status_code=%d, total_results=%d, num_entries=%d, query_title=%s", author, title, journal, max_results, str(feed), str(timestamp), response.status_code, total_results, num_entries, query_title)

    return feed, timestamp, response.status_code, total_results, num_entries, query_title


# Processes the feed data parsed by feedparser and structures it for response.
def process_feed(feed):
    logger.info("process_feed(feed): called: len(feed)=%d", len(feed))
    logger.debug("process_feed(feed): str(feed)=%s", str(feed))

    results = []
    for entry in feed.entries:
    
        # Process authors
        if hasattr(entry, 'authors'):
            authors_list = entry.get('authors', ["No author available"])
            authors = ', '.join( [author.name for author in authors_list] )
        else:
            authors = "No authors available"
            
        result = {
            "authors": authors,
            "title": getattr(entry, 'title', ''),
            "journal": getattr(entry, 'arxiv_journal_ref', '')
        }
        results.append(result)

    logger.debug("process_feed(feed): str(feed)=%s returning: %s", str(feed), str(results))

    return results

