docker stop mongo-scc413
docker rm mongo-scc413
docker run -p 27017:27017 \
 --name mongo-scc413 \
  -d mongo:5.0.16
