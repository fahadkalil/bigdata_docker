/*  
Para executar use:
  sql-client.sh -f mongodb_cdc.sql
*/

SET execution.checkpointing.interval = 3s;
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
    'hosts' = 'mongo:27017',
    'database' = 'mgdb',
    'collection' = 'orders',
	'scan.startup.mode' = 'initial'
    );

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
