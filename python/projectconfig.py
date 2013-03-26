# Author:  Adam Anderson
# Depends on:  Python 3.3
# Created:  February 12, 2012
# Updated:  March 25th, 2013

import configparser

# Create a config parser and read in the properties
config = configparser.RawConfigParser()
config.read('serial.cfg')


class SerialConfig(object):
    """ A class that contains all the config properties for Serial communication
        with the Arduino.
    """

    # The serial port's identifier (this is '/dev/tty/AM0' on Unix-like systems or 'COM4' on windows systems)
    port      = config.get('serial', 'port')

    # The baudrate to use for serial communications.
    baud      = config.getint('serial', 'baud')

    # The 'go-ahead' byte configured, if any.  When the serial port
    # receives this byte it knows its okay to transmit more bytes to
    # the target device.
    readybyte = config.getint('serial', 'readybyte')

    # the configured 'wait byte', if any.  When the SerialPort gets
    # this byte it waits until receiving the readbyte before continuing
    # to xmit more data.
    waitbyte  = config.getint('serial', 'waitbyte')
