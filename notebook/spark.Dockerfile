FROM docker.io/bitnami/spark:3.3
USER root
RUN install_packages curl
USER 1001
RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector/10.0.5/mongo-spark-connector-10.0.5.jar --output /opt/bitnami/spark/jars/mongo-spark-connector-10.0.5.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.5.0/mongodb-driver-sync-4.5.0.jar --output /opt/bitnami/spark/jars/mongodb-driver-sync-4.5.0.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/4.5.0/mongodb-driver-core-4.5.0.jar --output /opt/bitnami/spark/jars/mongodb-driver-core-4.5.0.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/bson/4.5.0/bson-4.5.0.jar --output /opt/bitnami/spark/jars/bson-4.5.0.jar
