import paho.mqtt.client as mqtt
import time

class Courier:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.client = mqtt.Client(self.name)
        self.client.connected_flag = False
        self.topics = {}

    def subscribe(self):
        formatted_topics = []
        for topic in self.topics.keys():
            formatted_topics.append((topic, 0))
        self.client.subscribe(formatted_topics)

    def configured_on_message_callback(self):
        def on_message_callback(client, userdata, msg):
            if msg != None:
                payload = msg.payload.decode("utf-8")
                callback = self.topics[msg.topic]
                callback(payload)
        return on_message_callback

    def configured_on_connect_callback(self):
        def on_connect_callback(client, userdata, flags, retCode):
            if retCode == 0:
                print ("Host connection successful! Return code: {}".format(retCode))
                self.client.connected_flag = True
                self.subscribe()
            else:
                print ("Host connection failed! Return code: {}".format(retCode))
        return on_connect_callback


    def establish_connection(self):
        try:
            self.client.on_connect = self.configured_on_connect_callback()
            self.client.on_message = self.configured_on_message_callback()
            self.client.connect(self.ip, port=self.port)
        except Exception as e:
            print(e)
            self.client.disconnect()

    def add_topic(self, topic, callback):
        self.topics[topic] = callback

    def run(self):
        self.establish_connection()
        try:
            self.client.loop_forever()
            while not self.client.connected_flag:
                print("Waiting to connect to host...")
                time.sleep(1)
        except Exception as e:
            print("Disconnecting from host with exception: {}".format(e))
            self.client.loop_stop()
            self.client.disconnect()
