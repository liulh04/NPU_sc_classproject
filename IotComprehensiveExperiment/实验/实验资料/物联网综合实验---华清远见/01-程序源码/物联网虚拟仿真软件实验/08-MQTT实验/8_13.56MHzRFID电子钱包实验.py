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
  print('MQTT Connect')
  hqyj_mqtt_clt.client.subscribe('AIOTSIM2APP', qos=0)

  hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"id":0,"module":"RFID_1356M","value":0,"mode":"05","data":[{"block_num":5}]}),ensure_ascii=False))
  time.sleep(3)
  hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"id":0,"module":"RFID_1356M","value":100,"mode":"03","data":[{"block_num":5}]}),ensure_ascii=False))
  print('Recharge 100')
  time.sleep(3)
  while True:
    hqyj_mqtt_clt.client.publish('APP2AIOTSIM', payload=json.dumps(({"id":0,"module":"RFID_1356M","value":10,"mode":"04","data":[{"block_num":5}]}),ensure_ascii=False))
    print('Deduct 10')
    time.sleep(3)
