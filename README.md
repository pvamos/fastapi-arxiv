# fastapi-arxiv-sqlalchemy

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

# to reduce data volume
- ArXiv Query: 
- unix timestamp
- minify

# to make scalable
- async + repliaction with outside sequential ID generation -> it will have correct data to query EVENTUALLY -> filter out too new based on timestamp :)

https://fastapi.tiangolo.com/async/

31.01.24: - Rebase to Alpine 3.19.
https://hub.docker.com/r/linuxserver/syslog-ng



Logging from your Python code
https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.25/administration-guide/17#TOPIC-1349350

Storing messages in plain-text files
https://www.syslog-ng.com/technical-documents/doc/syslog-ng-open-source-edition/3.25/administration-guide/34#TOPIC-1349417

Mount Filesystems Within a Docker Container
https://www.baeldung.com/linux/docker-mount-host-filesystem


How To Write Unit Tests For Existing Python Code 
https://www.youtube.com/watch?v=ULxMQ57engo

https://github.com/ArjanCodes/2022-test-existing-code


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