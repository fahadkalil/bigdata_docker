# Exemplo de Uso

- `api_clima.py`: Obtém dados de API pública e envia para tópico no Kafka
- `clima_jobpipeline.py`: Define pipeline para o Flink que consome mensagens do Kafka e encaminha para o MongoDB