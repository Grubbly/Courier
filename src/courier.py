import paho.mqtt.client as mqtt
import src.courier_logger as CourierLogger
import time
import json
from datetime import datetime

class Courier:
    def __init__(self, name, ip, port, logpath=None, monitor=False):
        self.name = name
        self.ip = ip
        self.port = port
        self.client = mqtt.Client(self.name)
        self.client.connected_flag = False
        self.topics = {}

        self.logger = CourierLogger.CourierLogger(path=logpath)
        self.logger.info("Courier instance name: {}".format(self.name))
        
        self.monitorPath = "monitor/src/data/mqtt_data.json"
        self.monitor = monitor
        if self.monitor:
            self.resetMonitor()

    def resetMonitor(self):
        with open(self.monitorPath, 'w') as file:
            file.write("""{"topics": [],"current": {},"history": {}}""")

    def monitorTopic(self, topic):
        with open(self.monitorPath, 'r') as file:
            data = json.load(file)
        data['topics'].append(topic)
        with open(self.monitorPath, 'w') as file:
            json.dump(data, file)

    def monitorCurrent(self, topic, val):
        with open(self.monitorPath, 'r') as file:
            data = json.load(file)
        data['current'][topic] = val
        with open(self.monitorPath, 'w') as file:
            json.dump(data, file)

    def monitorHistory(self, topic, val):
        with open(self.monitorPath, 'r') as file:
            data = json.load(file)

        if topic not in data['history']:
            data['history'][topic] = []

        data['history'][topic].append({
            "payload": val,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S %p")
        })
        with open(self.monitorPath, 'w') as file:
            json.dump(data, file)

    def log(self, type, msg):
        if type == "info":
            self.logger.info(msg)
        elif type == "warning":
            self.logger.warning(msg)
        elif type == "error":
            self.logger.error(msg)
        else:
            self.logger.debug(msg)

    def subscribe(self):
        formatted_topics = []
        for topic in self.topics.keys():
            self.logger.info("Subscribed to topic: {}".format(topic))
            formatted_topics.append((topic, 0))
        self.client.subscribe(formatted_topics)

    def configured_on_message_callback(self):
        def on_message_callback(client, userdata, msg):
            if msg != None:
                payload = msg.payload.decode("utf-8")
                self.logger.info("Topic: {} received the payload: {}".format(msg.topic, payload))
                
                if self.monitor:
                    self.monitorCurrent(msg.topic, payload)
                    self.monitorHistory(msg.topic, payload)

                callback = self.topics[msg.topic]
                callback(payload)
        return on_message_callback

    def configured_on_connect_callback(self):
        def on_connect_callback(client, userdata, flags, retCode):
            if retCode == 0:
                good_msg = "Host connection successful! Return code: {}".format(retCode)
                print (good_msg)
                self.logger.info(good_msg)
                self.client.connected_flag = True
                self.subscribe()
            else:
                err_msg = "Host connection failed! Return code: {}".format(retCode)
                print (err_msg)
                self.logger.error(err_msg)
        return on_connect_callback

    def establish_connection(self):
        try:
            self.logger.info("Attempting to establish connection to {}:{}".format(self.ip, self.port))
            self.client.on_connect = self.configured_on_connect_callback()
            self.client.on_message = self.configured_on_message_callback()
            self.client.connect(self.ip, port=self.port)
        except Exception as e:
            print(e)
            self.logger.error("Exception occured MQTT connection - disconnecting courier client...")
            self.client.disconnect()

    def add_topic(self, topic, callback):
        self.topics[topic] = callback
        self.logger.info("Added topic: {}".format(topic))
        self.monitorTopic(topic)

    def run(self):
        self.establish_connection()
        try:
            self.client.loop_forever()
            while not self.client.connected_flag:
                pending_msg = "Waiting to connect to host..."
                print(pending_msg)
                self.logger.warning(pending_msg)
                time.sleep(1)
        except Exception as e:
            err_msg = "Disconnecting from host with exception: {}".format(e)
            print(err_msg)
            self.logger.error(err_msg)
            self.client.loop_stop()
            self.client.disconnect()
