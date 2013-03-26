# Adam Anderson
# Depends on:  Python 3.3, PySerial 2.6
# Created:  February 12, 2012
# Updated:  March 25, 2013

from projectconfig import SerialConfig

import serial
import threading
import time

# --------------------------------------------------------------------------
# SerialPort
# --------------------------------------------------------------------------
# The SerialPort object wraps the Serial Port provided by the pyserial project
# to provide a dirt simple, easy to manipulate API.
#
# At construction the SerialPort starts listening for incoming data.  A custom
# LoopbackHandler can be created and provided to handle incoming data.
# --------------------------------------------------------------------------

class SerialPort(object):
    """ This is the primary communication class of the project.  This
        class manages and uses the Serial Port connection.
    """
    
    def __init__(self):
        """
        """
        # True if this SerialPort is listening to a loopback on the 
        # serial port.
        self.__loopback = False
        
        # The handler for loopback data.
        self.__loopbackHandler = None
        
        # True if the target device is ready to receive more bytes.
        self.__targetDeviceReady = True
        
        # Starts the listening thread.  This thread listens for 'ready'
        # messages from the target device and changes the value of
        # self.__targetDeviceReady.
        thread = threading.Thread(target=self.__listen)
        thread.start()

        # lock for making boolean access threadsafe.
        self.__lock = threading.Lock();

        # Initialize the pyserial serial port object that this object wraps.
        config = SerialConfig()
        self.__serialPort = serial.Serial(config.port, baudrate=config.baud)
        
        #ready and wait
        self.__ready = config.readybyte
        self.__wait = config.waitbyte


    def sendBytes(self, bites):
        """ Sends an array of bytes via this serial port.
    
            Parameters:
                bites   - a List of Bytes to send.
        """
        for bite in bites:
            self.sendByte(bite)

    def sendByte(self, bite):
        """ Sends a byte into the serial port.

            Parameters:
                bite - a single Byte to send.
        """
        # Verify the device is ready.
        while not self.__targetDeviceReady:
            # If not ready, wait 0.01 seconds and check again.
            print("Waiting...")
            time.sleep(0.001)

        self.__serialPort.write(bite)

    def startLoopback(self, loopbackHandler=DefaultLoopbackHandler()):
        """ Enables loopback for debug purposes using the provided 
            LoopbackHandler.
            
            Parameterss:
                loopbackHandler     The handler for loopback data.  If not 
                                    specified, a DefaultLoopbackHandler is
                                    used which prints out the data to the 
                                    console.
        """
        self.__loopbackHandler = loopbackHandler
        self.__loopback = True
        
    def endLoopback(self):
        """ Turns off loopback for debug purposes.
        """
        self.__loopback = False
        self.__loopbackHandler = None
            
    def __listen(self):
        while(True):
            byteValue = self.__serialPort.read()
            intValue = int.from_bytes(byteValue, byteorder='little')
            
            # if loopback is activated, print the received byte 
            # to the screen.  This should be updated to allow the user
            # of this API to supply a function that accepts an int as
            # a parameter.  This function will be called here in order
            # to enable users to define how they want to
            # use the loopback values.
            if (self.__loopback):
                self.__loopbackHandler.handleByte(intValue)
            
            # Listen for the 'ready' and 'not ready' commands coming 
            # back the target device and indicate as appropriate.
            if (intValue == self.__wait):
                # Update Ready State.
                self.__lock.acquire()
                try:
                    if self.__targetDeviceReady:
                        self.__targetDeviceReady = False
                finally:
                    self.__lock.release()
                
            elif(intValue == self.__ready):
                # Update Ready State.
                self.__lock.acquire()
                try:
                    if not self.__targetDeviceReady:
                        self.__targetDeviceReady = True
                finally:
                    self.__lock.release()
