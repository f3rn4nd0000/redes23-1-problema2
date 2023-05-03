import random
import time
from paho.mqtt import client as mqtt_client

class Publisher():

    def __init__(self, topic):
        self.broker = "localhost"
        self.port = 1883
        self.topic = topic
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'

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

    def publish(self, client, msg: dict):
        msg_count = 0
        while True:
            time.sleep(1)
            # msg = f"messages: {msg_count}"
            result = client.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{self.topic}`")
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg_count += 1

    def run(self):
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client)


if __name__ == '__main__':
    Publisher().run()
