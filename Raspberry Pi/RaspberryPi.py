import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO  # Import the GPIO library for Raspberry Pi
import json

# Define GPIO pins for controlling lights (replace with your actual pin numbers)
light1_pin = 17
light2_pin = 18

# MQTT broker details
broker_address = "smart_lights.iot.us-east-1.amazonaws.com"  # Replace with your AWS IoT Core endpoint
port = 8883  # MQTT secure port
control_topic = "lights/control"
brightness_topic = "lights/brightness"

# MQTT client setup
client = mqtt.Client(client_id="raspberry_pi_light_controller")
client.tls_set(ca_certs="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-certificate.pemcrt", certfile="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-public.pem.key", keyfile="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-private.pem.key")

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(light1_pin, GPIO.OUT)
GPIO.setup(light2_pin, GPIO.OUT)
pwm1 = GPIO.PWM(light1_pin, 100)  # Frequency set to 100 Hz
pwm2 = GPIO.PWM(light2_pin, 100)  # Frequency set to 100 Hz

# Function to control lights based on MQTT messages
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    topic = message.topic
    
    if topic == control_topic:
        handle_control_message(payload)
    elif topic == brightness_topic:
        handle_brightness_message(payload)

def handle_control_message(payload):
    # Parse the JSON message to extract the light ID and state
    data = json.loads(payload)
    light_id = data.get("light_id")
    state = data.get("state")
    
    if light_id == "light1":
        if state == "on":
            GPIO.output(light1_pin, GPIO.HIGH)  # Turn on the light
        elif state == "off":
            GPIO.output(light1_pin, GPIO.LOW)  # Turn off the light
    elif light_id == "light2":
        if state == "on":
            GPIO.output(light2_pin, GPIO.HIGH)  # Turn on the light
        elif state == "off":
            GPIO.output(light2_pin, GPIO.LOW)  # Turn off the light


def handle_brightness_message(payload):
    brightness = int(payload)
    data = json.loads(payload)
    light_id = data.get("light_id")
    state = data.get("state")
    
    if light_id == "light1":
        if 0 <= brightness <= 100:
            duty_cycle = brightness  # Map 0-100 to 0-100% duty cycle
            pwm1.ChangeDutyCycle(duty_cycle)
            print(f"Set brightness to {brightness}%")
        else:
            print("Invalid brightness value. Please use a value between 0 and 100.")
    elif light_id == "light2":
         if 0 <= brightness <= 100:
            duty_cycle = brightness  # Map 0-100 to 0-100% duty cycle
            pwm2.ChangeDutyCycle(duty_cycle)
            print(f"Set brightness to {brightness}%")
        else:
            print("Invalid brightness value. Please use a value between 0 and 100.")

# Configure MQTT message callbacks
client.on_message = on_message

# Connect to the MQTT broker and subscribe to topics
client.connect(broker_address, port)
client.subscribe(control_topic)
client.subscribe(brightness_topic)

# Start the MQTT client loop to listen for messages
client.loop_forever()
