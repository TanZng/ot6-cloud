FROM docker.io/bitnami/mongodb:6.0
USER root
RUN chown -R 1001:root /bitnami/mongodb
RUN chown -R 1001:root /bitnami/mongodb/data
USER 1001
RUN mkdir -p /bitnami/mongodb
RUN mkdir -p /bitnami/mongodb/data