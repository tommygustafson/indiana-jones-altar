# Indiana Jones - Fertility Idol Altar
This is the code that connects the PN532 RFID reader, activates the linear actuator and can also communicate with other devices with ESP322 radio

- Pi 3 or pi zero W2-> runs altar_pn532.py which drives the PN532 RFID reader, controls linear actuator and sends commands to other devices with ESP322 radio
- Pi 3 -> runs listen-act.py, which receives the RFID key tag string via ESP322 and can then act based on this tag

Setting up OS for raspberry pi:
- Install current headless version of Raspberry pi OS with Raspberry Pi Imager
- Install CircuitPython
- - https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
  - Need to run the command "source env/bin/activate" everytime the pi reboots
- Install gh (github desktop) to allow for persistent login:
- - https://docs.github.com/en/github-cli/github-cli/quickstart
  - https://github.com/cli/cli/blob/trunk/docs/install_linux.md
  - Needs personal token: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic
- Otherwise, git is used for version control
- - Git commit -am “commit notes”
  - Git push origin main   # pushes changes on pi’s to GitHub
  - Git pull origin main  # pulls or gets files from Github to pi
- Enable SPI 1
  - https://tutorials.technology/tutorials/69-Enable-additonal-spi-ports-on-the-raspberrypi.html
  - To enable spi1 also another line to the /boot/firmware/config.txt
    - dtoverlay=spi1-3cs
  - Double check with command: ls /dev/spidev*
    - Should see somthing like: 
    - /dev/spidev0.0  /dev/spidev0.1  /dev/spidev1.0  /dev/spidev1.1  /dev/spidev1.2
- Use Visual Code Studio running on main PC to edit code directly on Raspberry Pi using "Remote SSH" plugin
  - https://www.raspberrypi.com/news/coding-on-raspberry-pi-remotely-with-visual-studio-code/
  - https://randomnerdtutorials.com/raspberry-pi-remote-ssh-vs-code/

Useful linux commands:
- To see running python scripts: ps aux | grep python
- Options for connecting to output from an already running python program:
  - https://forums.raspberrypi.com/viewtopic.php?t=99257

Libraries needed:
- CircuitPython
  - Already installed during setup of raspberry pi
- Adafruit_pn532
  - pip3 install adafruit-circuitpython-pn532
- Circuitpython-nrf24l01
  - pip3 install circuitpython-nrf24l01
  - Documentation and info on wiring:
    - https://circuitpython-nrf24l01.readthedocs.io/en/latest/

PN_532 setup
- Uses 4 pins, plus a Vcc and Gnd
- By default, will use SPI 0 bus
- https://pinout.xyz/pinout/spi
- - Vcc is 3.3v
  - SCK (on red PN532) connects to SCLK (GPIO 11)
  - MISO (on red PN532) connects to MISO (GPIO 9)
  - MOSI (on red PN532) connects to MOSI (GPIO 10)
  - SS (on red PN532) connects to GPIO 5

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
    --> pip3 install adafruit-circuitpython-pn532
  - https://circuitpython-nrf24l01.readthedocs.io/en/latest/
    --> Installing the nrf libraries, wiring, pinouts for the NRF42l01 wireless transceiver



