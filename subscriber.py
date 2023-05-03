# python3.6

import random

from paho.mqtt import client as mqtt_client

class Subscriber():

    def __init__(self, topic):
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic = topic
        self.client_id = f'python-mqtt-{random.randint(0, 100)}'


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


    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        client.subscribe(self.topic)
        client.on_message = on_message


    def run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()


if __name__ == '__main__':
    Subscriber().run()
