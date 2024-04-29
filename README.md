# fastapi-arxiv-sqlalchemy

## Project organization

I've created separate stateless microservices:
-
-

I'm starting the containers waiting for each-other, like FastAPI endpoints container waits until PostgreSQL DB is listening.

## wait-for.sh

I've solved this waiting with this side-quest, I refactored a 4 years old sript to also work on Alpine Linux's ash shell provided by BusyBox:

https://github.com/pvamos/wait-for
Pure POSIX bash/ash script that will wait until response from a host and TCP port, then execute a command. 


The code contains all API endpoints together, it needs minimal effort to keep only 

These database tables are used:

```sql
-- For storing query metadata
CREATE TABLE queries (
    id SERIAL PRIMARY KEY,   -- ID and primary key
    query_id BIGINT,         -- Unique identifier of the query (from sequence, same as in the results table)
    timestamp BIGINT,        -- Unix timestamp of the query (same as in the results table)
    status SMALLINT,         -- HTTP status code of the response
    num_results SMALLINT,    -- Number of results found reported by the query
    num_entries SMALLINT,    -- Number of result entries returned (and stored) by the query
    query TEXT               -- The actual query string sent to arXiv
);

-- For storing individual results from each query
CREATE TABLE results (
    id SERIAL PRIMARY KEY,   -- ID and primary key
    query_id BIGINT,         -- Unique identifier of the query (from sequence, same as in the queries table)
    timestamp BIGINT,        -- Unix timestamp of the result (same as in queries table)
    result_number SMALLINT,  -- The sequential number of result for the query
    author TEXT,             -- Author(s) of the publication
    title TEXT,              -- Title of the publication
    journal TEXT             -- Journal reference, if available
);
```

The database tables are handled independently, they can even be on separate systems.


# to reduce data volume
- ArXiv Query: 
- unix timestamp
- minify

# to make scalable
- async + repliaction with outside sequential ID generation -> it will have correct data to query EVENTUALLY -> filter out too new based on timestamp :)

Performance tips:
- async operatons (and logging)
- connection pooling
- caching (Redis? Memcached?)
- fast JSON serializers
- payload trim / compression

Use path based routing to send API endpoints to separate containers

Separate into stateless microservices what can scale

# Unit Testing
Decompose into many small functions that can be tested separately: much less complex testing

How To Write Unit Tests For Existing Python Code 
https://www.youtube.com/watch?v=ULxMQ57engo

https://github.com/ArjanCodes/2022-test-existing-code


# to reduce data volume
- ArXiv Query: 
- unix timestamp
- minify

# to make scalable
- async + repliaction with outside sequential ID generation -> it will have correct data to query EVENTUALLY -> filter out too new based on timestamp :)

https://fastapi.tiangolo.com/async/

31.01.24: - Rebase to Alpine 3.19.
https://hub.docker.com/r/linuxserver/syslog-ng


# Logging

I use `logging` module from Python's standard library.
I'm logging to the container logs, the underlying container platform can simply collect it.

The most containerization solutions (including Docker and Kubernetes) can send the container logs to standardized external logging systems, like:
- syslog / syslog-ng / rsyslog
- Logstash -> ELK
- fluentd -> Elasticsearch, MongoDB...
- HDFS
- S3
- Graylog
- Google / Amazon cloud logging
- ...
 
Python's `logging` module supports only these 5 levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

Implemented the `NOTICE` standard syslog level "missing" from python logging.

```python
import logging

# Add custom NOTICE logging level
logging.NOTICE = 25
logging.addLevelName(logging.NOTICE, "NOTICE")

# Add custom NOTICE logging level
def notice(self, message, *args, **kws):
    if self.isEnabledFor(logging.NOTICE):
        self._log(logging.NOTICE, message, args, **kws)

# Attaching the custom method to Logger class
logging.Logger.notice = notice
```

I use these levels:
- `ERROR`:  Impacting errors
- `WARN`:   Error but not impacting, like error formatting one of the returned parameter values (returning none...)
- `NOTICE`: Log messages of normal operation, like the API endpoint calls
- `INFO`:   Less detailed debug-ish logs, like function calls with parameter values
- `DEBUG`:  Detailed debug logs, like function return values

The logging configuration is in `fastapi/app/main.py`.


# How to scale the solution


The project is organized into separate stateless microservice API endpoints.

Kubernetes has extensive horizontal pod autoscaling capabilities for Deploments, Docker Swarm can also scale replicated services.

Each endpoint can also scale horizontally in more "manual" way behind a HAProxy or similar.

The incoming external API requests can also be distributed with some proxy/reverse proxy solution capable of HTTP request path based routing, like HAProxy, Nginx, etc, or some cloud providers solution.


Separate the writable databas(e) from the readable database(s).



Writable PostgreSQL databases can scale less easily with active-active replication.

Database read operations can scale relatively easily, if we 

If we really need robust write performance, we should use a scaleable DB solution, like MongoDB.

If we expect load spikes, then we should use a message queing or stream processing solution in front of PostgreSQL, like Kafka, Nifi, RabbitMQ or similar, to buffer and manage data flows efficiently, ensuring system stability and performance scalability.


https://www.haproxy.com/blog/path-based-routing-with-haproxy

https://www.designgurus.io/blog/horizontally-scale-sql-databases

https://info.arxiv.org/help/api/user-manual.html

Implementing Async Logging in FastAPI Middleware
https://medium.com/@dresraceran/implementing-async-logging-in-fastapi-middleware-b112aa9c0db8

Top 7 Ways to 10x Your API Performance 
https://www.youtube.com/watch?v=zvWKqUiovAM

Fast-API with DB Connection Pools
In this API, we will see how to make an API with DB connection pools using FastAPI and SQLAlchemy. So that we can make our application more scalable and efficient.
We will make a user model in Fast API and Postgres database. We will use SQLAlchemy as an ORM to interacting with the database.
https://blog.devgenius.io/fast-api-with-db-connection-pools-cdfd6000827

How PostgreSQL Pipeline Mode Works
https://www.percona.com/blog/how-postgresql-pipeline-mode-works/

Open sourcing our fork of PgBouncer
PgBouncer will hold a pool of maximum server-side connections to Postgres, allocating those across multiple tenants to prevent Postgres connection starvation. From here, PgBouncer will forward backend queries to HAProxy, which load balances across Postgres primary and read replicas.
https://blog.cloudflare.com/open-sourcing-our-fork-of-pgbouncer



https://www.middlewareinventory.com/blog/deploy-docker-image-to-kubernetes/
