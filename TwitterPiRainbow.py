#!/usr/bin/python
import TwitterCreds
import re
import time
import RPi.GPIO as GPIO
from twython import TwythonStreamer

# Search terms
TERMS = '#dhfcolor'

# Board pin number of LED
REDLED = 12
GREENLED =16 
BLUELED =18 

# Use for white balancing
MAXRED=100
MAXBLUE=100
MAXGREEN=100

#Define Color Words
colors = ["aqua","black","blue","cyan","white","green","magenta","navy","orange","pink","purple","red","teal","yellow"]

#define colors
aqua=[0,255,255]
black=[0,0,0]
blue=[0,0,255]
cyan=[0,255,255]
white=[255,255,255]
green=[0,255,0]
magenta=[255,0,255]
navy=[0,0,128]
orange=[255,165,0]
pink=[255,192,203]
purple=[128,0,128]
red=[255,0,0]
teal=[0,128,128]
yellow=[255,255,0]

#Function to convert HTML color to RGB
def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

# Setup callbacks from Twython Streamer
class BlinkyStreamer(TwythonStreamer):
        def on_success(self, data):
                if 'text' in data:
                        print data['text'].encode('utf-8')
			for color in colors:
				matchColor = ""
				matchColor = re.search(color,data['text'],re.M|re.I)
				if matchColor:
					print 'Changing to: ' + matchColor.group()
					print globals()[color]
					#Set color on rPi here
					OldRange = (255 - 0)
					NewRange = (100 - 0)
					oldRed=globals()[color][0]
					oldGreen=globals()[color][1]
					oldBlue=globals()[color][2]
					newRed = ((oldRed * MAXRED) / OldRange)
					newGreen=((oldGreen * MAXGREEN) / OldRange)
					newBlue=((oldBlue * MAXBLUE) / OldRange)
					print 'NewRed: ' + str(newRed)
					print 'NewBlue: ' + str(newBlue)
					print 'NewGreen: ' + str(newGreen)

					REDPWM.stop()
					GREENPWM.stop()
					BLUEPWM.stop()
					REDPWM.start(newRed)
					GREENPWM.start(newGreen)
					BLUEPWM.start(newBlue)					
					
			matchColor = ""
			matchColor = re.search('#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})',data['text'],re.M|re.I)
			if matchColor:
				print 'Changing to: ' + matchColor.group()
				print 'In RGB: ' + str(HTMLColorToRGB(matchColor.group())) 
			print
                        time.sleep(3.0)
                       

# Setup GPIO as output
GPIO.setmode(GPIO.BOARD)
GPIO.setup(REDLED, GPIO.OUT)
GPIO.setup(GREENLED, GPIO.OUT)
GPIO.setup(BLUELED, GPIO.OUT)

#Reset all the pins just in case the script crashed before
GPIO.cleanup()

#Now use the pins for real
GPIO.setmode(GPIO.BOARD)
GPIO.setup(REDLED, GPIO.OUT)
GPIO.setup(GREENLED, GPIO.OUT)
GPIO.setup(BLUELED, GPIO.OUT)

REDPWM = GPIO.PWM(REDLED, 70)
GREENPWM = GPIO.PWM(GREENLED,70)
BLUEPWM = GPIO.PWM(BLUELED,70)
#BLUEPWM.start(100)

print "Test routine"
print "Red"
REDPWM.start(100)
time.sleep(3.0)

print "Yellow"
REDPWM.stop()
GREENPWM.stop()
BLUEPWM.stop()
REDPWM.start(100)
GREENPWM.start(100)
time.sleep(3.0)

print "Green"
REDPWM.stop()
GREENPWM.stop()
BLUEPWM.stop()
GREENPWM.start(100)
time.sleep(3.0)

print "Blue"
REDPWM.stop()
GREENPWM.stop()
BLUEPWM.stop()
BLUEPWM.start(100)
time.sleep(3.0)

print "White"
REDPWM.stop()
GREENPWM.stop()
BLUEPWM.stop()
BLUEPWM.start(90)
REDPWM.start(100)
GREENPWM.start(70)
time.sleep(3.0)

print "Ready..."


while True:
	# Create streamer
	try:
        	stream = BlinkyStreamer(TwitterCreds.APP_KEY(), TwitterCreds.APP_SECRET(), TwitterCreds.OAUTH_TOKEN(), TwitterCreds.OAUTH_TOKEN_SECRET())
	        stream.statuses.filter(track=TERMS)
	except: 
		pass
