# Exemplo de uso: Flink CDC + MongoDB

## Informações gerais

    URL INSTÂNCIA (Single-node): mongodb://localhost:27017/?replicaSet=rs0

## Verifique se o container foi inicializado e abra um terminal vinculado a ele usando o comando

    docker exec -it mongo /bin/bash

Acesse o shell do mongodb:

    mongosh

## Agora, dentro do shell do mongodb (mongosh), digite a sequencia de comandos

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

## Agora é necessário incluir o conector do FlinkCDC-MongoDB no container 'flink-jobmanager'

Acesse o container 'flink-jobmanager' usando o comando em um terminal:

    docker exec -it flink-jobmanager /bin/bash

Agora execute o(s) seguinte(s) comando(s):

    cd /opt/flink/lib && wget https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-mongodb-cdc/3.2.0/flink-sql-connector-mongodb-cdc-3.2.0.jar

## Comandos no FlinkSQL

Acesse o cliente SQL usando o comando

    sql-client.sh

Agora dentro do shell (FLINK SQL), execute:

    SET execution.checkpointing.interval = 3s;

    -- set local time zone as Asia/Shanghai
    SET table.local-time-zone = Asia/Shanghai;

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
    'hosts' = 'localhost:27017',
    'database' = 'mgdb',
    'collection' = 'orders'
    );
    
    CREATE TABLE customers (
    _id STRING,
    customer_id INT,
    name STRING,
    address STRING,
    PRIMARY KEY (_id) NOT ENFORCED
    ) WITH (
    'connector' = 'mongodb-cdc',
    'hosts' = 'localhost:27017',
    'database' = 'mgdb',
    'collection' = 'customers'
    );

Vamos definir a tabela que agrega dados

    CREATE TABLE agg_orders (
    order_id INT,
    order_date TIMESTAMP_LTZ(3),
    customer_id INT,
    price DECIMAL(10, 5),
    product ROW<name STRING, description STRING>,
    order_status BOOLEAN,
    customer_name STRING,
    customer_address STRING,
    PRIMARY KEY (order_id) NOT ENFORCED
    ) WITH (
    'connector' = 'mongodb',
    'uri' = 'mongodb://localhost:27017/?replicaSet=rs0',
    'database' = 'mgdb',
    'collection' = 'agg_orders'
    );

E por fim, definir o *sink* (ou seja, o destino):

    INSERT INTO agg_orders
    SELECT o.order_id,
            o.order_date,
            o.customer_id,
            o.price,
            o.product,
            o.order_status,
            c.name,
            c. address
    FROM orders AS o
    LEFT JOIN customers AS c ON o.customer_id = c.customer_id;