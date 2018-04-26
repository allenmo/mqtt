# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import json

# BCM GPIO
pins = [17, 18, 27, 22, 23, 24, 25, 4]
def gpio_setup():
    # use BCM mode
    GPIO.setmode(GPIO.BCM)
    # All as output, LOW
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        
def gpio_destory():
    for pin in pins:
        GPIO.output(pin, GPIO.LOW)
        GPIO.setup(pin, GPIO.IN)
        
# callback func after connection success
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # subcribe topic after connection success
    client.subscribe("gpio")
    
# callback func after pub
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    #get pin and value from payload
    gpio = json.loads(str(msg.payload))
    
    if gpio['pin'] in pins:
        if gpio['value'] == 0:
            GPIO.output(gpio['pin'], GPIO.LOW)
        else:
            GPIO.output(gpio['pin'], GPIO.HIGH)
            
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    gpio_setup()
    
    try:
        client.connect("allstack.net", 1883, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        client.disconnect()
        gpio_destory()
        
