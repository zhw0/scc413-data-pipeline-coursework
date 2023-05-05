FROM apache/airflow:2.5.3-python3.7

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim postgresql-client-common postgresql-client dnsutils \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

COPY requirements.txt /
COPY --chown=airflow --chmod=777 entrypoint_script.sh /
COPY --chown=airflow:root fact_taskflow.py /opt/airflow/dags
COPY --chown=airflow:root weather_taskflow.py /opt/airflow/dags
COPY initdb /initdb

RUN pip install --no-cache-dir -r /requirements.txt

ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://airflow_user:airflow_pass@postgres-db:5432/airflow_db"
ENV AIRFLOW_CONN_CAT_API="http://cat-api:5000"
ENV AIRFLOW_CONN_USELESS_FACT_API="https://uselessfacts.jsph.pl/api/v2/facts/random"
ENV AIRFLOW_CONN_BLACK_HISTORY_API="https://rest.blackhistoryapi.io/fact/random?length=4096"
ENV AIRFLOW_CONN_MONGO_NET="mongo://mongo-db:27017"
ENV AIRFLOW_CONN_ELASTICSEARCH_LOC="http://elastic-net:9200"
ENV AIRFLOW_CONN_WEATHER_DB="postgresql+psycopg2://postgres:123456@postgres-db:5432/weather_db"
ENV AIRFLOW_CONN_WEATHER_API="https://archive-api.open-meteo.com/v1/archive"