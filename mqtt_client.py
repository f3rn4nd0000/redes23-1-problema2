from paho.mqtt.client import _UserData, Client
import uuid
import json

class MqttCliente:

    def __init__(self, topic:str, topic_publish: list = []) -> None:
        self.broker = "localhost"
        self.port = 1883
        self.client_id = uuid.uuid1()
        self.topic = topic
        self.topic_publish = topic_publish
        self.client_mqtt = Client(self.client_id)

    def connect_mqtt(self) -> Client:
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Conectado ao Broker!")
            else:
                print("Falha ao se conectar, código de erro: %d\n", rc)
        self.client_mqtt.on_connect = on_connect
        self.client_mqtt.connect(self.broker, self.port)
        print("Increveu-se no topico", self.topic)
        self.client_mqtt.subscribe(self.topic)
        self.client_mqtt.publish(self.topic)
        # for topic in self._topicsPublish:
        #     self._client_mqtt.publish(topic)
            
        return self.client_mqtt
    
    def receberDados(self):
        """Recebe as mensagens para atualizar dos topicos para o qual se inscreveu
        """
        def on_message(client, userdata, msg):
            mensagem = msg.payload
            if mensagem:
                self._msg = json.loads(mensagem)
                return mensagem
            
        self._client_mqtt.on_message = on_message
        self._client_mqtt.loop_start()
    
    def enviarDadosTopic(self, topic):
        try:
            msg = json.dumps(self._msg).encode("utf-8")
            result = self._client_mqtt.publish(topic, msg)
            if result[0] != 0:
                raise Exception("Mensagem não enviada para o topico "+"'"+topic+"'")
        except Exception as ex:
            print(ex)
            
    def enviarDados(self):
        try:
            msg = json.dumps(self._msg).encode("utf-8")
            print("Enviando mensagem para", self._topic)
            result = self._client_mqtt.publish(self._topic, msg)
            if result[0] != 0:
                raise Exception("Mensagem não enviada para o topico "+"'"+self._topic+"'")
        except Exception as ex:
            print(ex)
