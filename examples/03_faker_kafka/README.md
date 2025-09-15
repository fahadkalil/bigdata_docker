# Exemplo de uso: FlinkSQL: Faker (source) e Kafka (sink)

## Parte 1: Kafka-UI

Nesse exemplo, crie um tópico chamado 'orders' no Kafka através da interface [Kafka-UI](http://localhost:8080 'http://localhost:8080').

Esse tópico terá as configurações padrão e pode ser definido apenas com uma *partition*.

## Parte 2: Container 'flink-jobmanager'

⚠️ **AVISO**: Container 'flink-taskmanager' também precisa estar inicializado ⚠️

Verifique se o container foi inicializado e abra um terminal:

    docker exec -it flink-jobmanager /bin/bash

Dentro do container 'flink-jobmanager', crie o arquivo faker_kafka.sql com o seguinte conteúdo:

    CREATE TEMPORARY TABLE orders (
    `order_id` INT,
    `order_status` STRING
    )
    WITH (
    'connector' = 'faker',
    'fields.order_id.expression' = '#{number.numberBetween ''0'',''100''}',
    'fields.order_status.expression' = '#{Options.option ''RECEIVED'',''SHIPPED'',''CANCELLED'')}'
    );

    CREATE TEMPORARY TABLE kafka_sink_01 (  
    `order_id` INT,
    `order_status` STRING
    ) WITH ( 
    'connector' = 'kafka', 
    'topic' = 'orders', 
    'properties.bootstrap.servers' = 'kafka:9092', 
    'format' = 'json', 
    'scan.startup.mode' = 'earliest-offset' 
    ); 

    INSERT INTO kafka_sink_01
    SELECT * FROM orders;

**Importante**: Note que as colunas definidas no `sink` deverão ser as mesmas (nome e tipo de dados) definidas no `source`.

Execute o *script* para gerar o job no Flink:

    sql-client.sh -f faker_kafka.sql

## Parte 3: Conferindo os resultados

- Acesse o [Flink Dashboard](http://localhost:8081) e verifique à esquerda em 'Jobs / Running Jobs' se o job foi criado e está com o status `RUNNING`.

- Acesse o [Kafka-UI](http://localhost:8080 'http://localhost:8080') e confira a geração ininterrupta de mensagens geradas pelo Source (Faker) dentro do tópico 'orders'.
