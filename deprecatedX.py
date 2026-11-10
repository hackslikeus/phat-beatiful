#!/usr/bin/env python3

    # This script requires a Raspberry Pi 2, 3 or Zero. Circuit Python must
    # be installed and it is strongly recommended that you use the latest
    # release of Raspbian.

import subprocess
import time
import os
import board
import digitalio

print("press a button!") #used for testing

#Define our button selection- 5 buttons for station choices:

#First Button or FastFwd
button1 = digitalio.DigitalInOut(board.D5)
button1.direction = digitalio.Direction.INPUT
button1.pull = digitalio.Pull.UP

#Second Button or Rewind
button2 = digitalio.DigitalInOut(board.D13)
button2.direction = digitalio.Direction.INPUT
button2.pull = digitalio.Pull.UP

#Third Button or Play/Pause
button3 = digitalio.DigitalInOut(board.D6)
button3.direction = digitalio.Direction.INPUT
button3.pull = digitalio.Pull.UP

#Fourth Button or Volume UP
button4 = digitalio.DigitalInOut(board.D16)
button4.direction = digitalio.Direction.INPUT
button4.pull = digitalio.Pull.UP

#Fifth button or Volume Down
button5 = digitalio.DigitalInOut(board.D26)
button5.direction = digitalio.Direction.INPUT
button5.pull = digitalio.Pull.UP

#A shutdown button
button = digitalio.DigitalInOut(board.D3)
button7.direction = digitalio.Direction.INPUT
button7.pull = digitalio.Pull.UP

while True:

     if not button1.value:
        subprocess.call(['killall', 'mpg123'])
        print("fastforward pressed")
        os.system('mpg123 -f 7000 http://east-mp3-128.streamthejazzgroove.com/ &')
        print ("playing jazz groove")

     if not button2.value:
        print("rewind pressed")
        subprocess.call(['killall', 'mpg123'])
        os.system('mpg123 -f 7000 http://server1.chilltrax.com:9000/ &')
        print ("playing chilltrax")
        
     if not button3.value:
        subprocess.call(['killall', 'mpg123'])
        print("play / pause pressed")
        os.system('mpg123 -f 7000 http://lb.zenfm.be/zenfm.mp3 &')
        print ("playing zenfm")

     if not button4.value:
        subprocess.call(['killall', 'mpg123'])
        print("volume up pressed")
        os.system('mpg123 -f 7000 http://ice2.somafm.com/christmas-256-mp3 &')
        print("playing SomaFM Christmas")

     if not button5.value:
        subprocess.call(['killall', 'mpg123'])
        print("volume down pressed")
        os.system('mpg123 -f 7000 http://ice1.somafm.com/groovesalad-256-mp3 &')
        print ("playing groove salad")
        
     if not button7.value:  #put the pi to sleep
        subprocess.call(['shutdown', '-h', 'now'], shell=False)  

time.sleep(.25)

