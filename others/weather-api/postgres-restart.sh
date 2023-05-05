docker network rm scc413-network
docker network create scc413-network

docker stop postgres-db
docker rm postgres-db

docker stop grafana-server
docker rm grafana-server

docker build -t postgre-scc413:1.0 \
 ~/projects/scc413-data-pipeline-coursework/postgresql/

docker run --name postgres-db \
    -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=123456' \
    --network scc413-network --network-alias postgresql-net \
     postgre-scc413:1.0

# docker run -d --name grafana-server \
#     --network scc413-network --network-alias grafana-net \
#     -p 3000:3000 grafana/grafana-oss
