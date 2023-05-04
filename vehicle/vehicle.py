import uuid
import random
import json
import time
from threading import Thread
from paho.mqtt import client as mqtt_client

TENDENCIA_DESCARREGAMENTO = {
    "1": "LENTA",
    "2": "MEDIA",
    "3": "RAPIDA"
}

class Vehicle():

    def __init__(self, latitude, longitude) -> None:
        self.broker          = "172.16.103.6"
        self.port            = 1883
        self.topic           = "veiculo"
        self.client_id       = f'python-mqtt-{random.randint(0, 100)}'
        self.client_mqtt     = self.connect_mqtt()
        self.vehicle_id = f"vehicle-{str(uuid.uuid1())}"
        self.latitude  = latitude
        self.longitude = longitude
        self.battery_level = 100
        self.discharge_tendency = random.randint(1,3)
        self.quadrant = 0

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

    def send_data_to_server(self):
        while True:
            time.sleep(4)
            try:
                client = self.client_mqtt
                msg = self.to_json()
                print(f"Enviando mensagem {msg} para topico {self.topic}")
                result = client.publish(self.topic, msg)
                if result[0] != 0:
                    raise Exception(f"Mensagem não enviada para o topico {self.topic}")
            except Exception as ex:
                print(ex)

    def receive_data_from_server(self, client:mqtt_client):
        def on_message(client, userdata, msg):
            payload = msg.payload.decode()
            print(payload)
            if "menor/fila" in msg.topic:
                print(f"Diriga-se ao posto de id {payload}")
                # self.calculate_distance()
            else:
                print('alsdlasdklaskdlaskdlkalsdkl')
            return None
        client.subscribe(self.topic)
        client.on_message = on_message
        

    def discharge_tendency_to_str(self):
        return TENDENCIA_DESCARREGAMENTO[str(self.discharge_tendency)]

    def speed(self):
        """
            Retorna a velocidade do carro em km/hora
        """
        return 2*self.discharge_tendency

    def move_around(self, client):
        while True:
            self.latitude += self.speed()
            self.longitude += self.speed()
            self.battery_level -= self.discharge_tendency
            print(self.battery_level)
            if self.battery_level <= 20:
                print("ATENCAO!!! NECESSARIO REABASTECER")
                print(f"va para o posto {self.receive_data_from_server(client)}")
                time.sleep(5)
                self.battery_level = 100
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
    vehicle       = Vehicle(random.randint(-100,100), random.randint(-100,100))
    data_sender   = Thread(target = vehicle.send_data_to_server)
    data_receiver = Thread(target = vehicle.receive_data_from_server, args = [vehicle.client_mqtt])
    data_sender.start()
    data_receiver.start()
    # alter_consumption = Thread(target = vehicle.move_around, args = [vehicle.client_mqtt])
    # alter_consumption.start()