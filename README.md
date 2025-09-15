# Multi Container Docker para Pipeline em Big Data

    Web User Interface     | Host      | Port
    -----------------------|-----------|-------------
    Flink Dashboard UI     | localhost | 8081
    Kafka-UI               | localhost | 8080  (http)
    RabbitMQ Management UI | localhost | 15672 (http)
    
    Service                | Host      | Port
    -----------------------|-----------|-------------    
    Zookeeper              | zookeeper | 2181
    Kafka                  | kafka     | 9092
    RabbitMQ               | rabbitmq  | 5672 (amqp)
    MongoDB                | mongo     | 27017

### Docker Image modificada do Apache Flink 1.20.0
- https://hub.docker.com/r/fahadkalil/my-flink

#### Dentro do container 'flink-jobmanager'

- Python 3.11
- pyflink 1.20.0
- kafkacat
- Linux tools: nano / vim / less / gzip / zip / unzip / nc / ping
- JARs do Flink para: Connectors e Formats

---

## Primeiro uso (ou instalação limpa)

    git clone https://github.com/fahadkalil/bigdata_docker.git
    cd bigdata_docker
    docker-compose up -d --pull=always

## Atualizar repositório (bigdata_docker) e images+containers do Docker
    git pull
    docker compose up -d --pull=always
    
