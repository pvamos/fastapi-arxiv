-- Create the database for the arXiv project
CREATE DATABASE arxiv;

-- Connect to the database to proceed with table creation
\c arxiv

-- Create table for storing query metadata
CREATE TABLE queries (
    id SERIAL PRIMARY KEY,   -- ID and primary key
    query_id BIGINT,         -- Unique identifier of the query (from sequence, same as in the results table)
    timestamp BIGINT,        -- Unix timestamp of the query (same as in the results table)
    status SMALLINT,         -- HTTP status code of the response
    num_results SMALLINT,    -- Number of results found reported by the query
    num_entries SMALLINT,    -- Number of result entries returned (and stored) by the query
    query TEXT               -- The actual query string sent to arXiv
);

-- Create table for storing individual results from each query
CREATE TABLE results (
    id SERIAL PRIMARY KEY,   -- ID and primary key
    query_id BIGINT,         -- Unique identifier of the query (from sequence, same as in the queries table)
    timestamp BIGINT,        -- Unix timestamp of the result (same as in queries table)
    result_number SMALLINT,  -- The sequential number of result for the query
    author TEXT,             -- Author(s) of the publication
    title TEXT,              -- Title of the publication
    journal TEXT             -- Journal reference, if available
);

-- Creating indices for the queries table to optimize search by timestamp and query_id
CREATE INDEX idx_query_timestamp ON queries (timestamp);
CREATE INDEX idx_query_query_id ON queries (query_id);

-- Creating indices for the results table to optimize search by timestamp and query_id
CREATE INDEX idx_result_timestamp ON results (timestamp);
CREATE INDEX idx_result_query_id ON results (query_id);

-- Create user for read and write access
CREATE USER arxiv_rw WITH PASSWORD 'notsecurepassword';
GRANT CONNECT ON DATABASE arxiv TO arxiv_rw;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO arxiv_rw;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO arxiv_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO arxiv_rw;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO arxiv_rw;

-- Create user for read-only access
CREATE USER arxiv_ro WITH PASSWORD 'notsecurepassword';
GRANT CONNECT ON DATABASE arxiv TO arxiv_ro;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO arxiv_ro;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO arxiv_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO arxiv_ro;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT USAGE ON SEQUENCES TO arxiv_ro;

-- Revoke all rights from public role, tighten security
REVOKE ALL ON DATABASE arxiv FROM PUBLIC;

-- Create a separate database for managing sequences
CREATE DATABASE arxiv_sequence;

-- Connect to the newly created sequence database
\c arxiv_sequence

-- Create a sequence that increments by one
CREATE SEQUENCE arxiv_sequence
    INCREMENT 1
    START 1
    MINVALUE 1
    CACHE 1;

-- Create a read-only user for the arxiv_sequence database
CREATE USER arxiv_sequence WITH PASSWORD 'notsecurepassword';
GRANT CONNECT ON DATABASE arxiv_sequence TO arxiv_sequence;
GRANT USAGE ON SCHEMA public TO arxiv_sequence;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO arxiv_sequence;

-- Revoke general public access to tighten security
REVOKE ALL ON DATABASE arxiv_sequence FROM PUBLIC;
