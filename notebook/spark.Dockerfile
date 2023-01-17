FROM docker.io/bitnami/spark:3.3.0
USER root
RUN install_packages curl
USER 1001
RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector_2.12/3.0.2/mongo-spark-connector_2.12-3.0.2.jar --output /opt/bitnami/spark/jars/mongo-spark-connector_2.12-3.0.2.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.8.2/mongodb-driver-sync-4.8.2.jar --output /opt/bitnami/spark/jars/mongodb-driver-sync-4.8.2.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/4.8.2/mongodb-driver-core-4.8.2.jar --output /opt/bitnami/spark/jars/mongodb-driver-core-4.8.2.jar
RUN curl https://repo1.maven.org/maven2/org/mongodb/bson/4.8.2/bson-4.8.2.jar --output /opt/bitnami/spark/jars/bson-4.8.2.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/spark/mongo-spark-connector/10.0.5/mongo-spark-connector-10.0.5.jar --output /opt/bitnami/spark/jars/mongo-spark-connector-10.0.5.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-sync/4.5.0/mongodb-driver-sync-4.5.0.jar --output /opt/bitnami/spark/jars/mongodb-driver-sync-4.5.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongodb-driver-core/4.5.0/mongodb-driver-core-4.5.0.jar --output /opt/bitnami/spark/jars/mongodb-driver-core-4.5.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/bson/4.5.0/bson-4.5.0.jar --output /opt/bitnami/spark/jars/bson-4.5.0.jar
# RUN curl https://repo1.maven.org/maven2/org/mongodb/mongo-hadoop-core/1.3.0/mongo-hadoop-core-1.3.0.jar --output /opt/bitnami/spark/jars/mongo-hadoop-core-1.3.0.jar
# RUN curl https://repo1.maven.org/maven2/org/apache/spark/spark-core_2.13/3.3.1/spark-core_2.13-3.3.1.jar --output /opt/bitnami/spark/jars/spark-core_2.13-3.3.1.jar
