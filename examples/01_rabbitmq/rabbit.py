from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.rabbitmq import RMQConnectionConfig, RMQSource, RMQSink
from pyflink.common.serialization import SimpleStringSchema

env = StreamExecutionEnvironment.get_execution_environment()

##https://nightlies.apache.org/flink/flink-docs-master/api/python//_modules/pyflink/datastream/connectors/rabbitmq.html

# Create an RMQConnectionConfig instance using the Builder pattern
connection_config = RMQConnectionConfig.Builder() \
    .set_host("localhost") \
    .set_port(5672) \
    .set_virtual_host("/") \
    .set_user_name("rabbit") \
    .set_password("rabbit") \
    .set_automatic_recovery(True) \
    .set_prefetch_count(100) \
    .build()

# Configure RabbitMQ Source
source = RMQSource(
    connection_config,
    "fila01_source",
    use_correlation_id=False,
    deserialization_schema=SimpleStringSchema()
)

# Consume data from RabbitMQ
data_stream = env.add_source(source)

# Configure RabbitMQ Sink
sink = RMQSink(
    connection_config,
    "fila01_sink",
    serialization_schema=SimpleStringSchema()
)

# Write processed data to RabbitMQ
data_stream.add_sink(sink)

env.execute("PyFlink RabbitMQ Local Test")
