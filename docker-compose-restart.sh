docker compose down

# https://docs.docker.com/engine/reference/commandline/rmi/
docker rmi --force airflow-scc413:1.0
docker rmi --force postgres-scc413:1.0
docker rmi --force cat-fact-server:1.0
docker rmi --force grafana-scc413:1.0

docker build -t airflow-scc413:1.0 airflow/
docker build -t postgres-scc413:1.0 postgresql/
docker build -t cat-fact-server:1.0 cat-fact-server/
docker build -t grafana-scc413:1.0 grafana/

docker compose up