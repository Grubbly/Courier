import paho.mqtt.client as mqtt
import time

class CourierController:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.client = mqtt.Client(self.name)
        self.establish_connection()

    def configured_on_connect_callback(self):
        def on_connect_callback(client, userdata, flags, retCode):
            if retCode == 0:
                print ("Controller connection successful! Return code: {}".format(retCode))
            else:
                print ("Controller connection failed! Return code: {}".format(retCode))
        return on_connect_callback

    def establish_connection(self):
        try:
            self.client.on_connect = self.configured_on_connect_callback()
            self.client.connect(self.ip, port=self.port)
        except Exception as e:
            print(e)
            self.client.disconnect()

    def send(self, payload, topic):
        self.client.publish(topic, payload=payload)
        print("Sent {} to {}".format(payload, topic))
