FROM flink:1.20.0

LABEL org.opencontainers.image.authors="Fahad Kalil <fahadkalil@gmail.com>"

# Install python + other Linux tools
RUN set -ex; \
  apt-get update; \
  apt-get -y install python3; \
  apt-get -y install python3-pip; \
  apt-get -y install python3-dev; \
  apt-get -y install kafkacat; \
  apt-get -y install netcat-traditional; \
  apt-get -y install iputils-ping; \
  apt-get -y install nano; \
  apt-get -y install less; \
  apt-get -y install gzip; \
  apt-get -y install zip unzip; \  
  ln -s /usr/bin/python3 /usr/bin/python;

# Install pyflink
RUN set -ex; \
  python -m pip install --upgrade pip; \
  pip install apache-flink==1.20.0

WORKDIR /opt/flink
COPY --chown=flink:flink ./connectors/*.jar ./lib
COPY --chown=flink:flink ./formats/*.jar ./lib

COPY --chown=flink:flink ./binaries/*.tar.gz /tmp
RUN find /tmp -name 'flink*.tar.gz' -exec tar -xzvf {} -C /root/ \;

RUN rm /tmp/flink*.tar.gz

EXPOSE 8081
