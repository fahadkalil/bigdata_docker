import json
import requests

import uuid # novo import

# pip install confluent-kafka
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)

def obter_dados(lat=None, long=None):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": long,
        "current_weather": True,
        "hourly": "temperature_2m"
    }

    response = requests.get(url, params=params)
    data = response.json()

    return data

def gerar_mensagens(dados_json=None):
    msgs = []

    for i, item in enumerate(dados_json['hourly']['time']):
        content = {
            'latitude': dados_json['latitude'],
            'longitude': dados_json['longitude'],
            'timezone': dados_json['timezone']
        }
        content['hourly_time'] = item
        content['hourly_temperature'] = dados_json['hourly']['temperature_2m'][i]
        msgs.append(content)

    return msgs   ### ALTERADA 

# Callback de confirmação de envio
def verifica_envio(err, msg):
    if err is not None:
        print(f"Envio de mensagem falhou: {err}")
    else:
        print(f"Mensagem enviada para {msg.topic()} [{msg.partition()}]")

def enviar_kafka(msgs=[]):
    topic = 'apiclima'
    for msg in msgs:
        producer.produce(
            topic,
            key=str(uuid.uuid4()),
            value=json.dumps(msg), 
            callback=verifica_envio
        )

    producer.flush()

dados = obter_dados(-28.15, -52.23) 
msgs = gerar_mensagens(dados)
enviar_kafka(msgs)
