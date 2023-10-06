import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__smartlight__)

# MQTT broker details
broker_address = "smart_lights.iot.us-east-1.amazonaws.com"  # Replace with your AWS IoT Core endpoint
port = 8883  # MQTT secure port

# MQTT client setup
client = mqtt.Client(client_id="ec2_mqtt_handler")
client.tls_set(ca_certs="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-certificate.pemcrt", certfile="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-public.pem.key", keyfile="523baac66ad2180ebc0cfc0e7c1d9eff326263e3605daf6827ac737fefe479ff-private.pem.key")
client.connect(broker_address, port)

# MongoDB connection details
mongo_host = 'mongodb://localhost:27017/'
mongo_db_name = 'Smart_lights'

# Connect to MongoDB
client = MongoClient(mongo_host)
db = client[mongo_db_name]

# Function to publish MQTT messages
def publish_mqtt_message(topic, message):
    client.publish(topic, message)

# HTTP route to control lights
@app.route('/api/control_light', methods=['POST'])
def control_light():
    data = request.json
    light_id = data.get('light_id')
    state = data.get('state')
    
    # Validate input and control the light
    if light_id and state in ['on', 'off']:
        mqtt_topic = f'lights/control/'
        payload = f'{{"light_id":{light_id},"state": {state}}}'
        publish_mqtt_message(mqtt_topic, payload)
        return jsonify({'message': f'Light {light_id} is {state}'}), 200
    else:
        return jsonify({'error': 'Invalid request'}), 400

@app.route('/api/control_brightness', methods=['POST'])
def control_brightness():
    data = request.json
    light_id = data.get('light_id')
    brightness = data.get('brightness')
    
    # Validate input and control the brightness
    if light_id and isinstance(brightness, int) and 0 <= brightness <= 100:
        mqtt_topic = f'lights/brightness/'
        payload = f'{{"light_id":{light_id},"brightness": {brightness}}}'
        publish_mqtt_message(mqtt_topic, payload)
        return jsonify({'message': f'Brightness of Light {light_id} set to {brightness}%'}), 200
    else:
        return jsonify({'error': 'Invalid request'}), 400

# MQTT on_message handler
def on_message(client, userdata, message):
    # Handle incoming MQTT messages here
    payload = message.payload.decode('utf-8')
    topic = message.topic

# Configure MQTT message callback
client.on_message = on_message

# Subscribe to MQTT topics
client.subscribe('lights/control/#')  # Subscribe to all control topics

if __name__ == '__main__':
    client.loop_start()  # Start the MQTT client loop in the background
    app.run(host='0.0.0.0', port=80)  # Run the Flask app on port 80
