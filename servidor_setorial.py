import uuid
import random
import json
import math
from threading import Thread
from paho.mqtt import client as mqtt_client

TOPICOS = ["fila/posto", "carro/distancia", "veiculo/se_dirigindo"]

SETORES = {
    "0": "NORTE",
    "1": "SUL",
    "2": "LESTE",
    "3": "OESTE"
}

TAMANHO_MAX_FILA = 15

## Eh o servidor que vai representar um determinado posto
class ServidorSetorial():

    def __init__(self, topics: list, latitude, longitude) -> None:
        self.setor           = SETORES[random.randint(0,3)]
        self.broker          = "localhost"
        self.port            = 1883
        self.topics          = topics
        self.client_id       = f"python-mqtt-{random.randint(0, 100)}"
        self.client_mqtt     = self.connect_mqtt()
        self.latitude        = latitude
        self.longitude       = longitude
        self.server_id       = uuid.uuid1()
        self.tamanho_fila    = 0
        self.stations        = []
        self.stations_ids    = []
        self.stations_queues = []
        self.veiculos        = []

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    # Recebe mensagens de um topico especifico
    def receive_messages(self, topic):
        ...

    def receive_messages_all_topics(self):
        ...

    def calculate_distance(self, veiculo):
        return math.sqrt((self.latitude - veiculo.latitude)**2 + (self.longitude - veiculo.longitude)**2)
    
    def calculate_distance_from_car(self):
        for veiculo in self.veiculos:
            self.calculate_distance_from_car(veiculo)

    def to_json(self):
        return json.dumps({
            "posto_id": self.server_id,
            "tamanho_fila": self.tamanho_fila,
            "coordenadas": (self.latitude, self.longitude)
        })

    def send_message_to_centralized_server(self):
        ...

if __name__ == "__main__":
    servidor_setorial = ServidorSetorial(topics=TOPICOS)