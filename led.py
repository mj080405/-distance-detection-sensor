import paho.mqtt.client as mqtt
from gpiozero import LED
import json

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_SUB_TOPIC = "mobile/02/distance"

led = LED(23)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_SUB_TOPIC)

def on_message(client, userdata, message):
    data = json.loads(message.payload)
    distance = data["distance"]
    print("Received distance:", distance)
    if distance > 30:  # 임계값 설정
        led.on()
    else:
        led.off()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT)
client.loop_forever()