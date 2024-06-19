from time import sleep
import json
import RPi.GPIO as GPIO
import time
import board
import paho.mqtt.client as mqtt

GPIO.setmode(GPIO.BCM)

TRIG = 13
ECHO = 19

MQTT_HOST = "mqtt-dashboard.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL = 60
MQTT_PUB_TOPIC = "mobile/02/distance"


def measure_distance_and_send_mqtt(client): 
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    try:
        while True:
            GPIO.output(TRIG, False)
            time.sleep(0.5)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17000
            distance = round(distance, 2)

            print("Distance:", distance, "cm")
            client.publish(MQTT_PUB_TOPIC, json.dumps({"distance": distance}))

            sleep(1)

    except KeyboardInterrupt:
        GPIO.cleanup()

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)

try:
    measure_distance_and_send_mqtt(client)
except KeyboardInterrupt:
    print("종료합니다!!")
finally:
    client.disconnect()
