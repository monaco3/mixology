import sys
import time
from labjack import ljm
from labjack.ljm.ljm import log
import serial.tools.list_ports  # pip install pyserial
import serial as serial

from numpy import random
import logging

# Set up logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Add a handler to print messages on the console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)


def find_ports():
    ports = [port for port in serial.tools.list_ports.comports()]
    # logger.info("Com ports found: %s",ports)
    for port in ports:
        logger.info("Port: {}  Serialnumber: {}".format(port.device, port.serial_number))
    return ports


class SerialControl:
    def __init__(self, serial_number, port=None):
        self.serial_number = serial_number
        self.connection = None
        self.baudrate = 9600
        self.parity = 'N'
        self.bytesize = 8
        self.newline = '\r\n'
        self.port = port if port is not None else self.find_port()
        pass

    def find_port(self):
        port = None
        ports = [port.device for port in serial.tools.list_ports.comports() if port.serial_number == self.serial_number]
        if len(ports) == 1:
            port = ports[0]
        return port

    def connect(self):
        if self.connection is not None:
            return None
        connection = None
        try:
            connection = serial.Serial(port=self.port, baudrate=self.baudrate, parity=self.parity, stopbits=1,
                                       timeout=1, xonxoff=0, rtscts=0)
        except serial.SerialException as e:
            print(self.serial_number, 'Could not open serial port: %s' % e)
        self.connection = connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def write(self, command):
        try:
            out = command + self.newline
            # print(out.encode('utf-8').hex())
            self.connection.write(out.encode('utf-8'))
            self.connection.readline()
        except TypeError as e:
            logger.warning(self.serial_number, 'Serial connection disconnected')
            logger.warning(e)

    def read(self, command):
        try:
            out = command + self.newline
            # print(out.encode('utf-8'))
            # print(out.encode('utf-8').hex())
            self.connection.write(out.encode('utf-8'))
            sd = self.connection.readline().decode('utf-8')  # Read serial data
            # sd = self.connection.readline() # Read serial data
        except serial.SerialException as e:
            logger.warning(self.serial_number, 'No data received')
            logger.warning(e)
        except TypeError as e:
            logger.warning(self.serial_number, 'Serial connection disconnected')
            logger.warning(e)
        except Exception as e:
            logger.warning(self.serial_number, 'other error')
            logger.warning(e)
        else:
            return sd


class PCE_Scale:
    def __init__(self, serial_number, port=None):
        self.controller = SerialControl(serial_number, port)
        self.controller.connect()
        logger.info('Scale of type PCE-TB6 connected')

    def string_processer(self, string):
        logger.debug("raw string is: {}".format(string.encode('utf-8')))
        if len(string) < 2:
            return None
        sign = string[0]
        number = string[2:11]
        unit = string[12:14]
        test = string[14:17]
        try:
            number = float(number)
        except Exception as e:
            logger.info("raw string is: {}".format(string.encode('utf-8')))
            return None
        if unit != "g ":
            logger.warnnig('Units not gram')
        if "-" in sign:
            number = - number
        return number

    def tara(self):
        time.sleep(2)
        count = 0
        max_count = 10
        while count < max_count:
            sd = self.controller.read('ST')
            if 'MT' in sd:
                time.sleep(2)
                return 0
            time.sleep(count * 5 + 1)
            count = count + 1
            logger.warning("Retrying tara: x{}".format(count))
        logger.warning("Could not tara scale")

    def zero(self):
        self.controller.read('SZ')
        time.sleep(1)

    def stable_weight(self):
        count = 0
        max_count = 10
        while count < max_count:
            time.sleep(2)
            sd = self.controller.read('SI')
            if len(sd) > 10:
                return self.string_processer(sd)
            time.sleep(count * 5 + 1)
            count = count + 1
            logger.warning("Retrying stable weight: x{}".format(count))
        logger.warning("could not get stable weight: {}".format(sd))
        return self.current_weight()

    def current_weight(self):
        sd = self.controller.read('Sx1')
        if len(sd) < 2:
            logger.warning("could not get stable read: {}".format(sd))
            return 0
        return self.string_processer(sd)


def Initialise_Serial_Unit(type, serial_number):
    if type == 'PCE_TB6':
        return PCE_Scale(serial_number)
    pass


if __name__ == "__main__":
    logger.debug("Logging is configured.")

    find_ports()
    SC = Initialise_Serial_Unit('PCE_TB6', 'FT3F30X1A')

    # SC.tara()
    # SC.zero()
    # for i in range(8):
    print(SC.stable_weight())
    #    time.sleep((10-i)/10)



