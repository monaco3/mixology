import sys
import time
from labjack import ljm
from labjack.ljm.ljm import log
import serial.tools.list_ports #pip install pyserial
import serial
import logging
from numpy import random
logger = logging.getLogger(__name__)

def find_ports():
    ports = [port for port in serial.tools.list_ports.comports()]
    #logger.info("Com ports found: %s",ports)
    for port in ports:
        logger.info("Port: {}  Serialnumber: {}".format(port.device,port.serial_number))
    return ports

print(find_ports())

