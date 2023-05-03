import uuid
import random
import json
import math
from threading import Thread
from paho.mqtt import client as mqtt_client

SETORES = {
    "0": "NORTE",
    "1": "SUL",
    "2": "LESTE",
    "3": "OESTE"
}

## Eh o servidor que vai representar um determinado posto
class ServidorSetorial():

    def __init__(self, topic1, topic2, latitude, longitude) -> None:
        self.latitude        = latitude
        self.longitude       = longitude
        self.setor           = SETORES[random.randint(0,3)]
        self.broker          = "localhost"
        self.port            = 1883
        self.topic1          = topic1   #fila/posto
        self.topic2          = topic2   #carros/distancia
        self.client_id       = f'python-mqtt-{random.randint(0, 100)}'
        self.client_mqtt     = self.connect_mqtt()
        self.server_id       = uuid.uuid1()
        self.stations        = []
        self.stations_ids    = []
        self.stations_queues = []
        self.veiculos        = []

    def calculate_distance(self, veiculo):
        return math.sqrt((self.latitude - veiculo.latitude)**2 + (self.longitude - veiculo.longitude)**2)