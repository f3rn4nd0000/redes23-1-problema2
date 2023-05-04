import uuid
import random
import json
from threading import Thread
from paho.mqtt import client as mqtt_client

TOPICS = ["fila/posto", "veiculo", "menor/fila"]

class ServidorCentral():

    def __init__(self, topics):
        self.broker          = "172.16.103.6"
        self.port            = 1883
        self.topics           = topics
        self.client_id       = f'python-mqtt-{random.randint(0, 100)}'
        self.client_mqtt     = self.connect_mqtt()
        self.server_id       = uuid.uuid1()
        self.stations        = []
        self.stations_ids    = []
        self.stations_queues = []
        self.vehicles        = []

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

    def receive_message_from_station(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            payload = msg.payload.decode() 
            
            if payload:
                if msg.topic == "fila/posto":
                    station_data = json.loads(payload)
                    # print(station_data)
                    # print(station_data["station-id"])   #str
                    # print(station_data["queue-size"])   #int
                    if self.stations_ids.count(station_data["station-id"]) == 0:
                        self.stations.append(station_data)
                        self.stations_ids.append(station_data["station-id"])
                    else:
                        index = self.stations_ids.index(station_data["station-id"])
                        upgradeable_object = self.stations[index]
                        upgradeable_object["queue-size"] = station_data["queue-size"]
                        print(f"novo valor = {upgradeable_object}")
            # print(self.stations)
            return None
        for topic in self.topics:
            client.subscribe(topic)
            client.on_message = on_message

    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        for topic in self.topics:
            client.subscribe(topic)
            client.on_message = on_message

    def publish_message_to_cars(self, topic):
        msg = "posto de menor fila = {}"
        try:
            result = self.client_mqtt.publish(topic, msg)
            if result[0] != 0:
                raise Exception(f"Mensagem nao enviada para o topico {topic}")
        except Exception as e:
            print(e)

    def run(self):
        client = self.connect_mqtt()
        self.receive_message_from_station(client)
        self.publish_message_to_cars("menor/fila")
        client.loop_forever()

    def process_better_station(self):
        # SEMPRE INSERE NA PRIMEIRA POSIÇÃO O POSTO COM A MENOR FILA
        self.stations_queues.insert(0, self.binarySearch(self.stations_queues))

if __name__ == "__main__":
    server                   = ServidorCentral(TOPICS)
    threaded_server          = Thread(target = server.run).start()
    order_list               = Thread(target = server.stations.sort).start()
    # publish_messages_to_cars = Thread(target = server.publish_message_to_cars, args=["veiculo"]).start()
    
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