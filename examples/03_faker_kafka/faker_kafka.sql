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