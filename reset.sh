#!/usr/bin/env bash

alias dl="docker logs -f"

docker-compose down -v

docker-compose build

docker-compose up -d

docker ps -a



