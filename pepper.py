#!/usr/bin/env python

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

import paho.mqtt.client as mqtt

ip="192.168.4.29"

from optparse import OptionParser

memory = None
nav = None

def on_connect(client, userdata, flags, rc):
	print("Connected " + str(rc))
	client.subscribe("pepper/moveon")
	client.subscribe("pepper/welcome")
	client.subscribe("pepper/goodbye")

def on_message(client, userdata, msg):
	print(msg.topic + " " + str(msg.payload))
	
	global nav
	global tts

	if msg.topic == "pepper/welcome":
		tts.say("Welcome " + str(msg.payload))
	elif msg.topic == "pepper/goodbye":
		tts.say("Goodbye " + str(msg.payload))
	elif msg.topic == "pepper/moveon":
		# lihat  http://doc.aldebaran.com/2-1/naoqi/motion/alnavigation.html
		#nav.navigateTo(1.0, 0.0)
		tts.say("Navigating..")
	
	
def main():
	parser = OptionParser()
	parser.add_option("--pip", help="Parent broker port, the IP address", dest="pip")
	parser.add_option("--pport", help="Parent broker port, port address", dest="pport", type="int")
	parser.set_defaults(pip=ip, pport=9559)
	
	(opts, args_) = parser.parse_args()
	pip = opts.pip
	pport = opts.pport

	myBroker = ALBroker("myBroker", "0.0.0.0", 0, pip, pport)

	global nav
	global tts
	nav = ALProxy("ALNavigation")
	tts = ALProxy("ALTextToSpeech")

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	print "connecting"
	client.connect("192.168.4.73", 1883, 60)

	client.loop_forever()

if __name__ == "__main__":
	main()	

