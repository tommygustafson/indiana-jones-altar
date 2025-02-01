# Indiana Jones - Fertility Idol Altar
This is the code that connects the PN532 RFID reader, activates the linear actuator and can also communicate with other devices with ESP322 radio

- Pi zero -> runs altar_pn532.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio
- Pi 3 -> runs listen-act.py, which receives the RFID key tag string via ESP322 and can then act based on this tag

Libraries needed:
CircuitPython
- https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
- Need to run the command "source env/bin/activate" everytime the pi reboots

PN_532 setup
- Uses 4 pins, plus a Vcc and Gnd
- By default, will use SPI 0 bus
- https://pinout.xyz/pinout/spi
- - Vcc is 3.3v
  - SCK (on red PN532) connects to SCLK (GPIO 11)
  - MISO (on red PN532) connects to MISO (GPIO 9)
  - MOSI (on red PN532) connects to MOSI (GPIO 10)
  - SS (on red PN532) connects to CE0 (GPIO 8)

-------------------------------------

Wiring diagram and moduels used on Pi zero
- runs altar_pn532.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio

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

--------------------------------------

Tips for use of Git / Github:
- Git commit -am “commit notes”
- Git push origin main   # pushes changes on pi’s to GitHub
- Git pull origin main  # pulls or gets files from Github to pi

