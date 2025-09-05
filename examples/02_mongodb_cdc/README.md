# Exemplo de uso: Flink CDC + MongoDB

## Descrição

Nesse exemplo vamos explorar o uso do Flink CDC para monitorar alterações no MongoDB através do uso do FLINK SQL API.

O Flink CDC permite integração de dados em tempo real com baixa latência, tolerância a falhas e suporte para vários bancos de dados, simplificando fluxos de trabalho de dados modernos. Ainda, captura alterações de dados e alterações de esquema em tempo real, mantendo os pipelines atualizados.

<small>CDC significa Change Data Capture</small>

<img src="https://yqintl.alicdn.com/d00b9167fac91ed2f5bf71832c74d62c8ccd5dbf.png" alt="Cenário Flink CDC"/>
[Cenário Flink SQL](https://yqintl.alicdn.com/d00b9167fac91ed2f5bf71832c74d62c8ccd5dbf.png)

## Observações

Na [Compose Stack](https://github.com/fahadkalil/bigdata_docker) que estamos usando todos os serviços se comunicam como se estivessem em uma mesma rede.

Assim, o host dos serviços é o próprio nome do container e **não devemos** usar *localhost* nas definições.

## Parte 1: Container 'mongo' (mongodb)

Verifique se o container foi inicializado e abra um terminal vinculado

    docker exec -it mongo /bin/bash

Acesse o shell do mongodb

    mongosh

Dentro do shell do mongodb (mongosh), digite a sequência de comandos

    // 1. Alterar para database 'mgdb'
    use mgdb;

    // 2. Popular documento com dados
    db.orders.insertMany([
    {
        order_id: 101,
        order_date: ISODate("2020-07-30T10:08:22.001Z"),
        customer_id: 1001,
        price: NumberDecimal("50.50"),
        product: {
        name: 'scooter',
        description: 'Small 2-wheel scooter'
        },
        order_status: false
    },
    {
        order_id: 102, 
        order_date: ISODate("2020-07-30T10:11:09.001Z"),
        customer_id: 1002,
        price: NumberDecimal("15.00"),
        product: {
        name: 'car battery',
        description: '12V car battery'
        },
        order_status: false
    },
    {
        order_id: 103,
        order_date: ISODate("2020-07-30T12:00:30.001Z"),
        customer_id: 1003,
        price: NumberDecimal("25.25"),
        product: {
        name: 'hammer',
        description: '16oz carpenter hammer'
        },
        order_status: false
    }
    ]);

    db.customers.insertMany([
    { 
        customer_id: 1001, 
        name: 'Jark', 
        address: 'Hangzhou' 
    },
    { 
        customer_id: 1002, 
        name: 'Sally',
        address: 'Beijing'
    },
    { 
        customer_id: 1003,
        name: 'Edward',
        address: 'Shanghai'
    }
    ]);

## Parte 2: Container 'flink-jobmanager'

Verifique se o container foi inicializado e abra um terminal vinculado

⚠️ **AVISO**: Container 'flink-taskmanager' também precisa estar inicializado ⚠️

    docker exec -it flink-jobmanager /bin/bash

### Comandos no FlinkSQL

Acesse o cliente SQL usando o comando

    sql-client.sh

Execute primeiros os comandos

    SET execution.checkpointing.interval = 3s;

    SET table.local-time-zone = Asia/Shanghai;

Agora, insira um comando por vez

`Source: orders`

    CREATE TABLE orders (
        _id STRING,
        order_id INT,
        order_date TIMESTAMP_LTZ(3),
        customer_id INT,
        price DECIMAL(10, 5),
        product ROW<name STRING, description STRING>,
        order_status BOOLEAN,
        PRIMARY KEY (_id) NOT ENFORCED
        ) WITH (
        'connector' = 'mongodb-cdc',
        'hosts' = 'mongo:27017',
        'database' = 'mgdb',
        'collection' = 'orders',
        'scan.startup.mode' = 'initial'
        );

`Source: customers`

    CREATE TABLE customers (
        _id STRING,
        customer_id INT,
        name STRING,
        address STRING,
        PRIMARY KEY (_id) NOT ENFORCED
        ) WITH (
        'connector' = 'mongodb-cdc',
        'hosts' = 'mongo:27017',	
        'database' = 'mgdb',
        'collection' = 'customers'
        );

`Sink: agg_orders (que une dados das tabelas anteriores)`

    CREATE TABLE agg_orders (
        _id STRING,
        order_id INT,
        order_date TIMESTAMP_LTZ(3),
        customer_id INT,
        price DECIMAL(10, 5),
        product ROW<name STRING, description STRING>,
        order_status BOOLEAN,
        customer_name STRING,
        customer_address STRING,
        PRIMARY KEY (_id) NOT ENFORCED
        ) WITH (
        'connector' = 'mongodb',
        'uri' = 'mongodb://mongo:27017/?replicaSet=rs0',
        'database' = 'mgdb',
        'collection' = 'agg_orders'
        );

`Criação do INSERT INTO que irá materializar o sink agg_orders e submeter o job`

    INSERT INTO agg_orders
    SELECT  
            o._id as _id,
            o.order_id,
            o.order_date,
            o.customer_id,
            o.price,
            o.product,
            o.order_status,
            c.name,
            c.address
    FROM orders AS o
    LEFT JOIN customers AS c ON o.customer_id = c.customer_id;

---

### Apache Flink Dashboard

Acesse no navegador: <http://localhost:8081>

Verifique à esquerda em 'Jobs / Running Jobs' se o job ***insert-into_default_catalog.default_database.agg_orders*** foi criado e está com o status `RUNNING`.

## Parte 3: Container 'mongo'

### Realizando modificações nos dados de origem para acionar o CDC

Comandos no MongoDB (mongosh) após o job estar rodando no Flink

    db.orders.insert({ 
    order_id: 104, 
    order_date: ISODate("2020-07-30T12:00:30.001Z"),
    customer_id: 1004,
    price: NumberDecimal("25.25"),
    product: { 
        name: 'rocks',
        description: 'box of assorted rocks'
    },
    order_status: false
    });

    db.customers.insert({ 
    customer_id: 1004,
    name: 'Jacob', 
    address: 'Shanghai' 
    });

    db.orders.updateOne(
    { order_id: 104 },
    { $set: { order_status: true } }
    );

    db.orders.deleteOne(
    { order_id : 104 }
    );

### Faça uma consulta na *collection* gerada e verifique se os dados aparecem

    db.agg_orders.find();
