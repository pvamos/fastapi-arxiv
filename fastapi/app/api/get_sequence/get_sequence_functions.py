# app/api/get_sequence/get_sequence_functions.py

import psycopg2
from ..dependencies import sequence_psycopg2_connect_string
from fastapi import HTTPException
import logging

logger = logging.getLogger('fastapi')


# Retrieves a sequence value from the database using psycopg2.
# As there is a known issue with using sequences with sqlalchemy.
# Sqlalchemy has a known issue with Postgres Sequence objects.
# It is not able perform this simple query:  SELECT nextval('arxiv_sequence')
# So I'm forced to use psycopg2 for this.
async def retrieve_sequence_value():
    logger.info("retrieve_sequence_value() called")

    try:
        conn = psycopg2.connect(sequence_psycopg2_connect_string)
        logger.debug("retrieve_sequence_value() Succesfully connected to the Postgres SEQUENCE DB with psycopg2")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to database: {str(e)}")

    with conn.cursor() as curs:
        try:
            curs.execute("SELECT nextval('arxiv_sequence')")
            single_row = curs.fetchone()
            sequence_value = single_row[0] if single_row else None
            logger.debug("retrieve_sequence_value() returning: %s", sequence_value)

            return sequence_value

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to retrieve sequence value: {str(e)}")
        finally:
            conn.close()

