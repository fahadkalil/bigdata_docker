# Multi Container Docker para Pipeline em Big Data

    Web User Interface      | Host      | Port
    ------------------------|-----------|---------
    Flink Dashboard         | localhost | 8081
    Mongo Express (mongodb) | localhost | 8082
    Kafbat (Kafka)          | localhost | 8085    
    pgAdmin (postgres)      | localhost | 8084        
    Redis Insight (valkey)  | localhost | 5540
    RabbitMQ Management     | localhost | 15672
    
    Service                | Host          | Port
    -----------------------|---------------|-------------        
    Kafka                  | kafka         | 9092  (tcp)
    RabbitMQ               | rabbitmq      | 5672  (amqp)
    MongoDB                | mongo         | 27017 (tcp)
    Valkey (redis)         | valkey        | 6379  (tcp)
    PostgreSQL             | postgres      | 5432  (tcp)
    Kafka Connect          | kafka-connect | 8083  (tcp)

## Docker Image modificada do Apache Flink 1.20.0

- [https://hub.docker.com/r/fahadkalil/my-flink](https://hub.docker.com/r/fahadkalil/my-flink)

### Dentro do container 'flink-jobmanager'

- Python 3.11
- pyflink 1.20.0
- kafkacat
- Linux tools: nano / vim / less / gzip / zip / unzip / nc / curl / wget / ping
- JARs do Flink para: Connectors e Formats

---

## Primeiro uso (ou instalação limpa)

    git clone https://github.com/fahadkalil/bigdata_docker.git
    cd bigdata_docker
    docker compose up -d --pull=always

## Atualizar repositório (bigdata_docker) e images+containers do Docker

    git pull
    docker compose up -d --pull=always
    
