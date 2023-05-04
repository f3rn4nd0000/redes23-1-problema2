import uuid
import random
import json
from threading import Thread
from paho.mqtt import client as mqtt_client

TENDENCIA_DESCARREGAMENTO = {
    "1": "LENTA",
    "2": "MEDIA",
    "3": "RAPIDA"
}

class Vehicle():

    def __init__(self, latitude, longitude) -> None:
        self.vehicle_id = f"vehicle-{str(uuid.uuid1())}"
        self.latitude  = latitude
        self.longitude = longitude
        self.discharge_tendency = random.randint(1,3)

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

    def discharge_tendency_to_str(self):
        return TENDENCIA_DESCARREGAMENTO[str(self.discharge_tendency)]

    def speed(self):
        """
            Retorna a velocidade do carro em km/hora
        """
        return 2*self.discharge_tendency

    def move_around(self):
        self.latitude += self.speed()
        self.longitude += self.speed()
        print((self.latitude, self.longitude))

    def to_json(self):
        return json.dumps(
            {
                "vehicle_id": self.vehicle_id,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "tendencia_descarregamento": self.discharge_tendency_to_str(),
            }
        )

if __name__ == "__main__":
    vehicle = Vehicle("")
    data_sender = Thread(target = vehicle.send_data_to_server)
    alter_consumption = Thread(target = vehicle.move_around)
    data_sender.start()
    alter_consumption.start()