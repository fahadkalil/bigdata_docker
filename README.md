# Multi Container Docker para Pipeline em Big Data

### Service | Port
 - Zookeeper | 2181
 - Kafka | 9092
 - Kafka-UI | 8080
 - Flink (job manager) + UI | 8081
 - Flink (task manager)

### Dentro do container 'flink-jobmanager'
  - Python 3.11
  - pyflink 1.20.0
  - kafkacat
  - Linux tools: nano / less / gzip / zip / unzip
  - JARs do Flink para: Connectors e Formats
