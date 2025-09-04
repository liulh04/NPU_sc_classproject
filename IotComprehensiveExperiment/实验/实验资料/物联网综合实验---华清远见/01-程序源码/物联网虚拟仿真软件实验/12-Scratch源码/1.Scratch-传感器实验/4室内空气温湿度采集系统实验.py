# -*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
from queue import Queue
import json
import base64
import requests
import time

class HQYJMqttClient:
  def __init__(self, broker_ip: str, broker_port: int):
    self.mqtt_queue = Queue(255)
    self.is_connected = False
    self.client = mqtt.Client()
    self.client.on_message = self.on_message
    self.client.on_connect = self.on_connect
    self.rc = 100
    try:
      self.client.connect(broker_ip, broker_port, 3)
    except Exception as e:
      print(e)

  def on_message(self, client, userdata, message):
    msg = json.loads(message.payload.decode())
    self.mqtt_queue.put(msg)

  def on_connect(self, client, userdata, flags, rc):
    print("result code:", rc)
    self.rc = rc

# 注意：在websocket端口是9001，如使用Python代码，端口需手动改成1883。
hqyj_mqtt_clt = HQYJMqttClient('127.0.0.1', 1883)
hqyj_mqtt_clt.client.loop_start()
time.sleep(3)
if hqyj_mqtt_clt.rc == 0:
  print('MQTT connected')
  hqyj_mqtt_clt.client.subscribe('SoftWareToScratch', qos=0)

  while True:
    mqtt_data = hqyj_mqtt_clt.mqtt_queue.get()

    if ('hum' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
      print('Humidity:')
      print((float(mqtt_data["hum"])))
    mqtt_data = hqyj_mqtt_clt.mqtt_queue.get()

    if ('tem' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
      print('Temperature:')
      print((float(mqtt_data["tem"])))
