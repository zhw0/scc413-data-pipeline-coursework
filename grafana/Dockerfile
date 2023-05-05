FROM grafana/grafana-oss:9.5.1

COPY postgres-datasource.yaml /etc/grafana/provisioning/datasources

COPY dashboard-local.yaml /etc/grafana/provisioning/dashboards

ADD ./dashboards /var/lib/grafana/dashboards

ENV DS_POSTGRES=Postgres