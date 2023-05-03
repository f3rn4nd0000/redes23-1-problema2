import uuid
import random
import json
from threading import Thread
from paho.mqtt import client as mqtt_client

class ServidorCentral():

    def __init__(self, topic):
        self.broker          = "localhost"
        self.port            = 1883
        self.topic           = topic
        self.client_id       = f'python-mqtt-{random.randint(0, 100)}'
        self.client_mqtt     = self.connect_mqtt()
        self.server_id       = uuid.uuid1()
        self.stations        = []
        self.stations_ids    = []
        self.stations_queues = []

    def connect_mqtt(self) -> mqtt_client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)
        client = mqtt_client.Client(self.client_id)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    # It returns location of x in given array arr
    # if present, else returns -1
    def binarySearch(arr, left, right, value_to_be_searched):
        while left <= right:
            mid = left + (right - left) // 2
            # Check if value to be searched is present at mid
            if arr[mid] == value_to_be_searched:
                return mid
            # If value to be searched is greater, ignore left half
            elif arr[mid] < value_to_be_searched:
                left = mid + 1
            # If value to be searched is smaller, ignore right half
            else:
                right = mid - 1
        # If we reach here, then the element
        # was not present
        return -1

    def receive_message_from_station(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            payload = msg.payload.decode() 
            
            if payload:
                station_data = json.loads(payload)
                print(station_data["station_id"])   #str
                print(station_data["queue_size"])   #int
                if self.stations_ids.count(station_data["station_id"]) == 0:
                    self.stations.append(station_data)
                    self.stations_ids.append(station_data["station_id"])
                else:
                    index = self.stations_ids.index(station_data["station_id"])
                    upgradeable_object = self.stations[index]
                    upgradeable_object["queue_size"] = station_data["queue_size"]
                    print(f"novo valor = {upgradeable_object}")
            print(self.stations)
            return None
        
        client.subscribe(self.topic)
        client.on_message = on_message
        
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic)
        client.on_message = on_message

    def run(self):
        client = self.connect_mqtt()
        self.receive_message_from_station(client)
        client.loop_forever()

    def publish_message_to_cars(self):
        ...

    def process_better_station(self):
        # SEMPRE INSERE NA PRIMEIRA POSIÇÃO O POSTO COM A MENOR FILA
        self.stations_queues.insert(0, self.binarySearch(self.stations_queues))

if __name__ == "__main__":
    server = ServidorCentral("fila/posto").run()
    # server.receive_message_from_station(client = server.connect_mqtt())
    # receive_message_from_station(server.client_mqtt)
    # thread_server = Thread(target = server.receive_message_from_station, args = [server.client_mqtt]).start()


"""
    def receberDados(self):
        '''
        Recebe e gerencia as mensagens dos topicos para o qual o setor foi inscrito

        Returns:
            msg: mensagem de um determinado topico para o qual o setor se inscreveu
        '''
        while True:
            def on_message(client, userdata, msg):
                mensagem = msg.payload
                if mensagem:
                    mensagem = json.loads(mensagem)
                    if 'lixeira' in msg.topic:
                        Thread(target=self.gerenciarLixeiras, args=(mensagem, )).start()
                    else:
                        print(mensagem)
                return mensagem
            
            self.server.on_message = on_message
            self.server.loop_start()
"""    