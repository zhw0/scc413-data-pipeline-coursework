# scc413-data-pipeline-coursework

## API

https://github.com/public-apis/public-apis

https://github.com/wh-iterabb-it/meowfacts

```bash
curl http://127.0.0.1:5000
```

https://uselessfacts.jsph.pl/

```bash
curl https://uselessfacts.jsph.pl/api/v2/facts/random
```

https://www.blackhistoryapi.io/docs

```bash
curl -X 'GET' \
  'https://rest.blackhistoryapi.io/fact/random?length=4096' \
  -H 'accept: application/json' \
  -H 'x-api-key: aG9uZ3podmYxVGh1IEFwciAyMCAyMD'
```

## Airflow

Remove example dags.

https://stackoverflow.com/questions/43410836/how-to-remove-default-example-dags-in-airflow

Burn down and rebuild the metadata database

```bash
airflow db reset -y
```

Restart airflow.

```bash
airflow db reset -y && airflow standalone
```

Build docker image.

```bash
docker build -t airflow-scc413:1.0 .
```

Run container.

```bash
docker run -p 8080:8080 \
  --env "_AIRFLOW_DB_UPGRADE=true" \
  --env "_AIRFLOW_WWW_USER_CREATE=true" \
  --env "_AIRFLOW_WWW_USER_PASSWORD=admin" \
  --name 123 \
  airflow-scc413:1.0 airflow scheduler
```

```bash
docker run --name 123 \
 airflow-scc413:1.0 airflow db check
```

## MongoDB

```bash
docker run -p 27017:27017 \
 --name mongo-scc413 \
 --network scc413-network --network-alias mongo-net \
  -d mongo:5.0.16
```

## Docker

Display IDs of all containers.

```bash
docker ps --all --quiet
```

Display IDs of all images.

```bash
docker images --all --quiet
```

Remove all images.

```bash
docker rmi --force $(docker images --all --quiet)
```

Start a container and get into it.

```bash
docker run -it hello-world
```

## pgAdmin

### Docker

https://hub.docker.com/r/dpage/pgadmin4

https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html

```bash
docker run --name pgadmin-server \
    -p 8001:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=admin@123.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=123456' \
    -d dpage/pgadmin4:7.0
```

## PostgreSQL

https://hub.docker.com/_/postgres

https://github.com/docker-library/docs/blob/master/postgres/README.md

https://stackoverflow.com/questions/37694987/connecting-to-postgresql-in-a-docker-container-from-outside

To execute SQL at init step, we need to build a new image based on postgres image.

In postgres-docker directory, run the command

```bash
docker build -t postgres-scc413:1.0 .
```

default user name: postgres

```bash
docker run --name postgres-db \
    -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=123456' \
    -d postgres-scc413:1.0
```

### psql

install

```bash
sudo apt install -y postgresql-client-common
sudo apt install -y postgresql-client
```

connect

```bash
psql -h 127.0.0.1 -p 5432 -U postgres
```

List Databases

```sql
\list
```

### Postgre Airflow

```bash
docker network create scc413-network

docker build -t postgre-scc413:1.0 ~/projects/scc413-data-pipeline-coursework/postgres-docker/

docker run --name postgres-db \
    -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=123456' \
    --network scc413-network --network-alias postgresql-net \
    -d postgre-scc413:1.0

docker build -t airflow-scc413:1.0 ~/projects/scc413-data-pipeline-coursework/airflow-docker/

docker run -it --name 123 \
 -p 8080:8080 \
 --network scc413-network \
 airflow-scc413:1.0 airflow db check
```