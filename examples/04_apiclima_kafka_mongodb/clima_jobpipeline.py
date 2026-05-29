## REFERENCIA
## https://raw.githubusercontent.com/decodableco/examples/refs/heads/main/pyflink/pyflink_hello_world.py

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

def kafka_mongodb_pipeline():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)

    t_env = StreamTableEnvironment.create(stream_execution_environment=env)    	

    t_env.execute_sql("""
    CREATE TABLE kafka_source (
    `raw_value` STRING
    ) WITH (
    'connector' = 'kafka',
    'topic' = 'apiclima',
    'properties.bootstrap.servers' = 'kafka:9092',
    'properties.group.id' = 'apiclimaGroup',
    'scan.startup.mode' = 'earliest-offset',
    'format' = 'raw'  -- Treats the whole value as a string
    )""")
   
    t_env.execute_sql("""
    CREATE TABLE mongo_sink (    
    raw_value STRING
    ) WITH (
        'connector' = 'mongodb',
        'uri' = 'mongodb://mongo:27017',
        'database' = 'clima',
        'collection' = 'apiclima'
    )""")

    ## gerar o insert + select para ativar o pipeline
    t_env.execute_sql("""
    INSERT INTO mongo_sink
     SELECT * FROM kafka_source
    """)

if __name__ == '__main__':    
    kafka_mongodb_pipeline()