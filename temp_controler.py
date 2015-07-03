#!/usr/bin/env python2.7  

import sys
import re
import time
import datetime


from measurementClass import *
from thresholdsClass import *
from relaysClass import *
from graphClass import *


###Import GPI Library
# 
# sudo apt-get install python-dev python-rpi.gpio
import RPi.GPIO as GPIO
###SETUP GPIO
GPIO.setmode(GPIO.BCM)

HEAT_RELAY_PIN = 18
HUMIDITY_RELAY_PIN = 19
AIR_RELAY_PIN = 20

GPIO.setup(HEAT_RELAY_PIN, GPIO.OUT)
GPIO.setup(HUMIDITY_RELAY_PIN, GPIO.OUT)
GPIO.setup(AIR_RELAY_PIN, GPIO.OUT)

GPIO.output(HEAT_RELAY_PIN, GPIO.LOW)
GPIO.output(HUMIDITY_RELAY_PIN, GPIO.LOW)
GPIO.output(AIR_RELAY_PIN, GPIO.LOW)

###
#SETUP RELAY
heat_relay = relay("Heat",HEAT_RELAY_PIN)
humidity_relay = relay("Humidity",HUMIDITY_RELAY_PIN)
air_relay = relay("Air",AIR_RELAY_PIN)


#import Adafruit_DHT
#import this library and buld it:
#https://github.com/adafruit/Adafruit_Python_DHT.git
#git clone https://github.com/adafruit/Adafruit_Python_DHT.git
# apt-get update
# sudo apt-get install build-essential python-dev
#python setup.py build
# import dhtreader


MEASUREMENT_ARRAY_SIZE = 10000  # MEASUREMENT_ARRAY_SIZE x MEASUREMENT_TIME /(60*60)  = time in hours of measurements

#####
##SET UP Temperature Measurements class
temp1 = temperature("Temp1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class1 
temp2 = temperature("Temp1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class2
temp_classes = [temp1,temp2]

#####
##SET UP Humidity Measurements class
hum1 = humidity("Temp1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class1 
hum2 = humidity("Temp1",MEASUREMENT_ARRAY_SIZE) ## Name and size of the array. Set up temperature class2
hum_classes = [hum1,hum2]

###########################
##SET UP Thresholds#########
temperature_threshold = measurementThreshold("Temperature_threshold", 20, 2, 2, MEASUREMENT_ARRAY_SIZE)
humidity_threshold = measurementThreshold("Humidity Threshold", 80, 5, 2, MEASUREMENT_ARRAY_SIZE)

sensors_pins = [13,14] #used to specify nubmer of sensors and what pin they are. Should equal the number of temp, and should equal number of hum class
sensor_type = ["DHT22", "DHT22"]
#sensor1 = sensor_args[sys.argv[1]]

MEASUREMENT_TIME = 10 #time in seconds between measurement
RELAY_TIME = 20 # time in seconds between triggering relay

####
##Code for timing
measure_time = datetime.datetime.now()
relay_time = datetime.datetime.now()


########################
##CODE FOR SETUP HERE?##




#########################
##FOR LOOP STARTS HERE###
while True:

  if (datetime.datetime.now() - measure_time).total_seconds() > MEASUREMENT_TIME:
    measure_time = datetime.datetime.now()
    #######################################
    ##Check here the Lastest Readings##
    for counter, pin in enumerate(sensors_pins):
      humidity, temperature = (8, 21) #Adafruit_DHT.read_retry(sensor_type[counter], sensors_pins[counter])
      if humidity is not None and temperature is not None:
        temp_classes[counter].add_temperature(temperature)
        hum_classes[counter].add_humidity(humidity)
      else:
        print 'Failed to get reading for Sensor {0}. Try again!'.format(counter)
  ##################################
  ##END READING SENSOR CODE
  #################################


  ######################################
  ##Has Trigger Time passed#############
  if (datetime.datetime.now() - relay_time).total_seconds() > RELAY_TIME:
    relay_time = datetime.datetime.now()

    ####COMBIng THE ARRAYS AND SEND TO THRESHOLD CLASS
    temperature_arrays = []
    for classes in temp_classes:
      temperature_arrays.append(classes.temperature_array)   
    temperature_threshold.combine_measurements(temperature_arrays)
    
    ####COMBIng THE ARRAYS AND SEND TO THRESHOLD CLASS
    humidity_arrays = []
    for classes in hum_classes:
      humidity_arrays.append(classes.humidity_array)   
    humidity_threshold.combine_measurements(humidity_arrays)  


    ###################################
    ##Check if I should trigger
    if temperature_threshold.check_if_under:
      heat_relay.turn_on()
      print "Temperature too low"
    else:
      heat_relay.turn_off()
      print "Temperature too high"  

    if humidity_threshold.check_if_under:
      humidity_relay.turn_on()
      print "humidity too low"
    else:
      humidity_relay.turn_off()
      print "humidity too high"


  #Is time X Passed, if so trigger Air intake.












