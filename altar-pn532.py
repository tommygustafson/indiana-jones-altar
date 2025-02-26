"""
  Interface RFid PN-532 Reader using Python3 / CircuitPython on Raspberry Pi 3/4/Zero
  -- Pn-532 Library does NOT work on the Pico
  
  Turn off Wifi power management:
  [Consider using subprocess to call this at start of program]
  [https://www.circuitbasics.com/run-linux-commands-with-python/]
  run in terminal: sudo iw wlan0 set power_save off
  check: iw wlan0 get power_save
  should return: "Power save: off"
  EXAMPLE:
  import subprocess
  output = subprocess.run(['sudo iw wlan0 set power_save off'], shell=True, capture_output=True, text=True)
  #pass whole command as string
  print(output)
  
  Other libraries required:
  - adafruit_pn532
  - circuitpython_nrf24l01 (folder) (https://github.com/nRF24/CircuitPython_nRF24L01)
  
  References:
  – https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
    --> Installs circuit python libraries, checks a bunch of useful config items (SSH, SPI)
  - https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/spi-sensors-devices
    --> Info specifically on SPI bus
  - https://learn.adafruit.com/adafruit-pn532-rfid-nfc/python-circuitpython
    -->  Installing the PN532 libraries, wiring diagrams for the PN532 breakout board
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
    --> Installing the nrf libraries, wiring, pinouts for the NRF42l01 wireless transceiver
   
For Git:  Use PowerShell
Git commit -am “commit notes”
Git push origin main --> pushes changes to GitHub
Git pull origin main --> pulls / gets / updates files from Github
   
"""

import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import time
import struct
from datetime import datetime
from circuitpython_nrf24l01.rf24 import RF24
from adafruit_pn532.spi import PN532_SPI
import subprocess
import pygame
import pwmio
from threading import Timer

'''
###############
# Use Subprocess to ensure that wireless / Wifi power management is OFF
###############
'''
output = subprocess.run(['sudo iw wlan0 set power_save off'], shell=True, capture_output=True, text=True)
output2 = subprocess.run(['iw wlan0 get power_save'], shell=True, capture_output=True, text=True)
#pass whole command as string
#ouput2.stdout includes the return text, need to strip \n
output_txt = output2.stdout.strip()
if output_txt == 'Power save: off':
    print("WIFI POWER MANAGEMENT IS OFF")
else:
    print("WIFI POWER MANAGEMENT IS ON - NEED TO FIX")

'''
###############################
# Set up digital pins for control of relay
# input 1 = D.20
# input 2 = D.21

Also need to attach on relay, vcc to 5v on Rpi and gnd to ground on Rpi

###############################

'''

relay_1 = DigitalInOut(board.D27) #BLUE, IN1
relay_2 = DigitalInOut(board.D17) #GREEN, IN2

relay_1.direction = Direction.OUTPUT
relay_2.direction = Direction.OUTPUT

'''
#########################
# For relay outputs, a value of FALSE is ON / ACTIVE on relay
# and value of TRUE is OFF / INACTIVE on relay
#
# To extend linear actuator: relay_1 = True, relay_2 = False
# To retract linear actuator: relay_1 = False, relay_2 = True
# To pause / stop: relay_1 = True, relay_2 = True
##########################
'''

relay_1.value = True
relay_2.value = True

'''
####################################
# Set up output pins for motor controller (L298N) for rumble motor control
#
# Two digital outputs:
# rumble_1 = D23
# rumble_2 = D24
#
# no rumble when rumble_1 = rumble_2 = False
# yes rumbler with rumble _1 != rumble_2 (i.e. 1 = True, 2 = False)
#
# Uses 3rd pin for PWM output
# Uses pwmio library
# pwm = D18
# strenth of rumble is the percentage of 2 ** 16 duty cycle
# pwm.duty_cycle = max_duty_cycle
'''
print("#################")
print("setting up PWM for rumble motors")

max_duty_cycle = (2 ** 16) - 2
medium_duty_cycle = (2 ** 16) / 2
low_duty_cycle = (2 ** 16) / 4
off_duty_cycle = 0

rumble_1 = DigitalInOut(board.D23)
rumble_2 = DigitalInOut(board.D24)
pwm = pwmio.PWMOut(board.D18, frequency=50)
rumble_1.direction = Direction.OUTPUT
rumble_2.direction = Direction.OUTPUT

# Start with rumble OFF
rumble_1.value = False
rumble_2.value = False

def stop_rumble():
    rumble_1.value = False
    rumble_2.value = False

def start_rumble(duty_cycle):
    rumble_1.value = True
    rumble_2.value = False
    pwm.duty_cycle = duty_cycle

print("end set up of rumble motors")
print("#########################\n")

#def add_tag_to_list(tag_list, uid, pixels):
def add_tag_to_list(tag_list, uid):
    tag_str = ''
    tag_int = 0
    for i in uid:
        tag_str += str(i)
        tag_int += int(i)
    if tag_str not in tag_list:
        tag_list.append(tag_str)
        print("added tag ",tag_str," to tag list")
        #pixels.fill(GREEN)
    else:
        throw_away = 1
        #print("Tag ", tag_str, " already in list")
        #print("Sending tag_int = ", tag_int)
        #send_data_nrf(tag_int)
        #send_data_nrf(tag_str)
    return tag_str
'''
#######################################
# process_tag
# here, will perform actions / send nrf data based on tag
# Consider, taking no action if same tag present from cycle to cyle,
#   but will need to ensure we don't skip actions between long times of same tag
#
#######################################
'''

def process_tag(tag_list,uid,prior_tag_str):
    # TO DO: Make extend and retractor tag as lists to allow multiple tags / objects
    extend_actuator_tag = "8131164137"
    retract_actuator_tag = "8018321730"

    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
    print("date and time =", dt_string)

    tag_str = add_tag_to_list(tag_list,uid)
    print("Processing tag: ", tag_str)
    #print(tag_list)

    if prior_tag_str == tag_str:
        print("Same tag on sensor, take no action")
        #stop_actuator()
    else:
        print("New tag detected, taking action and send data")
        #send_data_nrf(tag_str)
        if tag_str == extend_actuator_tag:
            extend_actuator()
        if tag_str == retract_actuator_tag:
            retract_actuator()
            play_boulder_crash_mp3()
            start_rumble(low_duty_cycle)
            t = Timer(5, stop_rumble)
            t.start() # stop_rumble will be called after a 5 second interval


    # Return current tag_str to become prior_tag_str
    print("---------")
    return tag_str

def extend_actuator():
    print("Extending actuator")
    relay_1.value = False
    relay_2.value = True

def retract_actuator():
    print("Retracting actuator")
    relay_1.value = True
    relay_2.value = False

def stop_actuator():
    print("Stop actuator")
    relay_1.value = True
    relay_2.value = True

def is_actuator_moving():
    if relay_1.value == False or relay_2.value == False:
        return True
    else:
        return False

def play_boulder_crash_mp3():
    mp3file = "/home/tom/indiana-jones-altar/mp3/trimmed-boulder.mp3"
    pygame.mixer.init()
    pygame.mixer.music.load(mp3file)
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()

def send_data_nrf(data):
    #data = 1234
    #buffer = struct.pack("<i", int(data))
    buffer = struct.pack("<q", int(data))
    #################
    # in struct.pack, "i" uses a 4 byte int
    # "q" uses an 8 byte int
    #################

    print("Sending: {} as struct: {}".format(data, buffer))
    start_timer = time.monotonic() * 1000  # start timer
    result = nrf.send(buffer)
    end_timer = time.monotonic() * 1000  # end timer
    if not result:
        print("send() failed or timed out")
    else:
        print("send() successful")
        # print timer results despite transmission success
        print("Transmission took", end_timer - start_timer, "ms")


'''
#####
# Set up LED pin
#####
'''
#led = DigitalInOut(board.LED)
#led.direction = Direction.OUTPUT


'''
############################################
# SPI connection:
############################################

Set up SPI connection for the PN532 RFID reader

White = 3.3v
Black = Ground
Green / teal = SCK
Purple = MISO
Gray = MOSI
Blue = SCL / Rx / SSEL

'''
print("Starting setup of PN532")
spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
cs_pin = DigitalInOut(board.D5)
pn532 = PN532_SPI(spi, cs_pin, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

# Create string from hex code to compare items
tag_list = []
prior_tag_str = ""

'''
##################
# Set up nrf
##################
'''
print("Setting up nRF")
# addresses needs to be in a buffer protocol object (bytearray)
spi2SCLK = board.D21
spi2MOSI = board.D20
spi2MISO = board.D19
address = b"1Node"
#spi2 = busio.SPI(spi2SCLK, spi2MOSI, spi2MISO)
ce_nrf_pin = DigitalInOut(board.D6)
csn_nrf_pin = DigitalInOut(board.D13)

#nrf = RF24(spi, csn_nrf_pin, ce_nrf_pin)
#nrf.open_tx_pipe(address)  # set address of RX node into a TX pipe
#nrf.listen = False  # ensures the nRF24L01 is in TX mode

print("#######")
print("Setup of nRF completed")
print("#######")


print("#######")
print("Setup of PN532 completed")
print("#######")

print("Waiting for RFID/NFC card...")
while True:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    #pixels.fill(YELLOW)
    #pixels.show()
    #print(".", end="")
    # Try again if no card is available.
    if uid is None:
        prior_tag_str = ""
        if is_actuator_moving():
            stop_actuator()
        continue
    #print("Found card with UID:", [hex(i) for i in uid])
    #print("Found card with UID in str:", [str(i) for i in uid])
    prior_tag_str = process_tag(tag_list,uid,prior_tag_str)    
    time.sleep(0.5)
