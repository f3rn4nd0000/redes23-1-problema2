from threading import Thread
import uuid
import json
import random
import time
from paho.mqtt import client as mqtt_client

class Station():
    
    def __init__(self, topic):
        self.broker       = "172.16.103.6"
        self.port         = 1883
        self.topic        = topic
        self.client_id    = f'python-mqtt-{random.randint(0, 100)}'
        self.client_mqtt  = self.connect_mqtt()
        self.latitude     = random.randint(-100,100)
        self.longitude    = random.randint(-100,100)
        self.station_id   = f"posto-{uuid.uuid1()}"
        self.tamanho_fila = 0
        self.quadrant     = 0

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

    def send_data_to_server(self):
        while True:
            time.sleep(4)
            try:
                client = self.connect_mqtt()
                msg = self.to_json()
                print(f"Enviando mensagem {msg} para {self.topic}")
                result = client.publish(self.topic, msg)
                if result[0] != 0:
                    raise Exception(f"Mensagem não enviada para o topico {self.topic}")
            except Exception as ex:
                print(ex)

    def randomly_alter_queue(self):
        while True:
            time.sleep(1)
            self.tamanho_fila += random.randint(-1, 1)
            if self.tamanho_fila == 0:
                self.tamanho_fila += 1
            if self.tamanho_fila == 15:
                self.tamanho_fila -= 1

    def to_json(self):
        return json.dumps(
            {
                "station-id": self.station_id,
                "station-latitude": self.latitude,
                "station-longitude": self.longitude,
                "queue-size": self.tamanho_fila
            }
        )

if __name__ == "__main__":
    station = Station("fila/posto")
    print(station.latitude, station.longitude)
    data_sender = Thread(target = station.send_data_to_server)
    alter_queue = Thread(target = station.randomly_alter_queue)
    data_sender.start()
    alter_queue.start()
