#!/bin/bash
echo "Download last changes"
git pull

echo "Rebuild docker images"
docker-compose up --build --force-recreate --remove-orphans --no-deps -d

echo "Project started"