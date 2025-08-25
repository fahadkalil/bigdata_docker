# Exemplo de uso: Apache Flink e RabbitMQ

Nesse exemplo temos um pipeline (job) com duas filas (queues) no RabbitMQ, sendo uma definida como Source e outra como Sink através do uso da biblioteca PyFlink python que usa a biblioteca PyFlink.

É feito uso da classe de Serialização/Deserialização *SimpleStringSchema* para troca simples de mensagens.

Duas filas deverão estar definidas no RabbitMQ. Para isso, pode-se utilizar o RabbitMQ Management UI (http://localhost:15672) e as credenciais *rabbit* (username) e *rabbit* (password).

A criação das filas é feita na aba '*Queues and Streams*' na opção '*Add a new queue*'.

O nome das filas deverá ser, conforme a definição do arquivo [rabbit.py](rabbit.py) disponível:

- fila01_source
- fila01_sink

O objetivo do processamento do Apache Flink é monitorar '*fila01_source*' e encaminhar as mensagens para '*fila01_sink*'.

## Para executar o *job*

Acesse o container 'flink-jobmanager' usando o comando em um terminal:

    docker exec -it flink-jobmanager /bin/bash

Agora execute o(s) seguinte(s) comando(s) para incluir o arquivo '*rabbit.py*' no container e executar o *job*:

    cd && wget https://raw.githubusercontent.com/fahadkalil/bigdata_docker/refs/heads/main/examples/rabbit.py -O rabbit.py
    /opt/flink/bin/flink run -py rabbit.py

## Testando

No RabbitMQ Management UI, publique uma mensagem na fila '*fila01_source*' e depois verifique se esta foi encaminhada para a fila '*fila01_sink*'.