#!/usr/bin/env bash

docker stop $(docker ps --all --quiet)
docker rm $(docker ps --all --quiet)

# docker rmi --force $(docker images --all --quiet)
docker rmi --force postgre-scc413:1.0
docker rmi --force airflow-scc413:1.0
docker rmi --force cat-api:1.0

docker network rm scc413-network
docker network create scc413-network

docker run -p 27017:27017 \
 --name mongo-scc413 \
 --network scc413-network --network-alias mongo-net \
  -d mongo:5.0.16

docker build -t postgre-scc413:1.0 \
 ~/projects/scc413-data-pipeline-coursework/postgres-docker/

docker run --name postgres-db \
    -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=123456' \
    --network scc413-network --network-alias postgresql-net \
    -d postgre-scc413:1.0

docker build -t cat-api:1.0 ~/projects/meowfacts/

docker run --name cat-api \
 -d -p 5000:5000 \
 --network scc413-network --network-alias cat-api-net \
 cat-api:1.0

# docker run --name es01-test \
#   --net scc413-network --network-alias elastic-net \
#   -p 9200:9200 \
#   -p 9300:9300 \
#   -e "discovery.type=single-node" \
#   -d elasticsearch:7.17.9

# docker run --name kib01-test \
#  --net scc413-network \
#  -p 5601:5601 \
#  -e "ELASTICSEARCH_HOSTS=http://es01-test:9200" \
#  -d kibana:7.17.9

docker build -t airflow-scc413:1.0 \
 ~/projects/scc413-data-pipeline-coursework/airflow-docker/


docker run  \
  -p 8080:8080 \
  --name airflow-main \
  --network scc413-network \
  --env "_AIRFLOW_DB_UPGRADE=true"  \
  --env "_AIRFLOW_WWW_USER_CREATE=true" \
  --env "_AIRFLOW_WWW_USER_USERNAME=abc" \
  --env "_AIRFLOW_WWW_USER_PASSWORD=123456" \
  -d airflow-scc413:1.0 bash -c "/my_after_entrypoint_script.sh"
