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
time.sleep(1)
if hqyj_mqtt_clt.rc == 0:
  print('MQTT connected')
  hqyj_mqtt_clt.client.subscribe('AIOTSIM2APP', qos=0)

  while True:
    mqtt_data = hqyj_mqtt_clt.mqtt_queue.get()

    if ('infrared' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
      if (mqtt_data["infrared"]) == 1:
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"lamp":True, "id":0}),ensure_ascii=False))
      else:
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"lamp":False, "id":0}),ensure_ascii=False))
    if ('RFID_125K' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
      print((mqtt_data["RFID_125K"]))
      if str((mqtt_data["RFID_125K"])).find(str('5B3758B468')) > -1:
        print('Right person')
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"doorLock":True, "id":0}),ensure_ascii=False))
      else:
        print('Wrong person')
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"doorLock":False, "id":0}),ensure_ascii=False))
    if ('RFID_24G' in mqtt_data) and ('id' in mqtt_data) and (mqtt_data['id'] == 0):
      print((mqtt_data["RFID_24G"]))
      if str((mqtt_data["RFID_24G"])).find(str('304066DA')) > -1:
        print('Right car')
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"barrierGate":True, "id":0}),ensure_ascii=False))
      else:
        print('Wrong car')
        hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"barrierGate":False, "id":0}),ensure_ascii=False))
    time.sleep(3)
    hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"barrierGate":False, "id":0}),ensure_ascii=False))
    hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"doorLock":False, "id":0}),ensure_ascii=False))

