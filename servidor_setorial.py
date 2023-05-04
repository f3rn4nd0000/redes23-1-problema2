import uuid
import random
import json
import math
import time
from threading import Thread
from paho.mqtt import client as mqtt_client

TOPICOS = ["fila/posto", "menor/fila"]
# TOPICOS = ["fila/posto","carro/distancia","veiculo/se_dirigindo"]
TAMANHO_MAX_FILA = 15

SETORES = {
    "0": "NORTE",
    "1": "SUL",
    "2": "LESTE",
    "3": "OESTE"
}

## Eh o servidor que vai representar um determinado posto
class ServidorSetorial():

    def __init__(self, topics: list, latitude, longitude) -> None:
        self.setor           = SETORES[str(random.randint(0,3))]
        self.broker          = "localhost"
        self.port            = 1883
        self.topics          = topics
        self.client_id       = f"python-mqtt-{random.randint(0, 100)}"
        self.client_mqtt     = self.connect_mqtt()
        self.latitude        = latitude
        self.longitude       = longitude
        self.server_id       = uuid.uuid1()
        self.tamanho_fila    = 0
        self.veiculos        = []
        self.quadrant        = 0
   
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

    def return_vehicle_quadrant(self, latitude, longitude) -> bool:
        if latitude > 0 :
            if longitude > 0:
                self.quadrant = 1
            else:
                self.quadrant = 4
        elif longitude < 0:
            self.quadrant =2
        else:
            self.quadrant = 3

    # Recebe mensagens de um topico especifico
    def receive_messages(self, client):
        def on_message(client, userdata, msg):
            print((self.latitude, self.longitude))
            payload = msg.payload.decode()
            if "fila/posto" in msg.topic:
                print(payload)
                # print("devemos calcular a distancia entre o veiculo e o carro")
            elif "veiculo/se_dirigindo" in msg.topic:
                print("veiculo se dirigindo para o posto")
                self.tamanho_fila += 1
            elif "carro/distancia" in msg.topic:
                # AQUI VAI PEGAR A DISTANCIA DO CARRO ATRAVES DE SEUS ATRIBUTOS
                # payload.
                self.calculate_distance()
        client.subscribe(self.topics)
        client.on_message = on_message

    def receive_messages_all_topics(self):
        for topic in self.topics:
            self.receive_messages(topic)

    def calculate_distance(self, veiculo):
        return math.sqrt((self.latitude - veiculo.latitude)**2 + (self.longitude - veiculo.longitude)**2)
    
    def calculate_distance_from_car(self):
        for veiculo in self.veiculos:
            self.calculate_distance(veiculo)

    def to_json(self):
        return json.dumps({
            "posto_id": str(self.server_id),
            "tamanho_fila": self.tamanho_fila,
            "coordenadas": (self.latitude, self.longitude)
        })

    def send_message_to_centralized_server(self, topic):
        msg = self.to_json()
        try:
            result = self.client_mqtt.publish(topic, msg)
            if result[0] != 0:
                raise Exception(f"Mensagem nao enviada para o topico {topic}")
        except Exception as e:
            print(e)

    def run(self):
        client = self.connect_mqtt()
        self.receive_messages(client)
        self.send_message_to_centralized_server(topic="fila/posto")
        client.loop_forever()

if __name__ == "__main__":
    servidor_setorial_um     = ServidorSetorial(latitude=50, longitude=50, topics=TOPICOS)
    servidor_setorial_dois   = ServidorSetorial(latitude=-50, longitude=50, topics=TOPICOS)
    servidor_setorial_tres   = ServidorSetorial(latitude=-50, longitude=-50, topics=TOPICOS)
    servidor_setorial_quatro = ServidorSetorial(latitude=50, longitude=-50, topics=TOPICOS)

    thread_um     = Thread(target=servidor_setorial_um.run).start()
    thread_dois   = Thread(target=servidor_setorial_dois.run).start()
    thread_tres   = Thread(target=servidor_setorial_tres.run).start()
    thread_quatro = Thread(target=servidor_setorial_quatro.run).start()