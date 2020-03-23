import paho.mqtt.client as mqtt

class Courier:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.client = mqtt.Client(self.name)

    def establish_connection(self):
        try:
            self.client.connect(self.ip, self.port)
        except Exception as e:
            print(e)
            self.client.disconnect()

    