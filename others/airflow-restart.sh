docker stop $(docker ps --all --quiet)
docker rm $(docker ps --all --quiet)

docker network rm scc413-network
docker network create scc413-network

docker run --name postgres-db \
    -p 5432:5432 \
    -e 'POSTGRES_PASSWORD=123456' \
    --network scc413-network --network-alias postgresql-net \
    -d postgre-scc413:1.0

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
   airflow-scc413:1.0 bash -c "/my_after_entrypoint_script.sh"