# Adam Anderson
# Depends on:  Python 3.3
# Created:  March 25, 2013
# Updated:  March 25, 2013

# --------------------------------------------------------------------------
# Whats a loopback handler?
# --------------------------------------------------------------------------
# Loopback handlers define and interface for how received bytes should be
# handled.  Whenever a byte is received by a serial port, if loopback is
# activated for the serial port, the loopback handler is called to 'handle'
# the newly received byte.
#
# Two simple LoopbackHandlers are defined here - the default one simply 
# prints out each byte.  The Logging handler writes each byte to a file.
# Consider writing your own loopback handler for whatever your project
# requires.
# --------------------------------------------------------------------------

class DefaultLoopbackHandler(object):
    """ A simple, loopback handler that simply prints out the bytes 
        received by this serial port to the console.
    """
    
    def handleByte(self, intByte):
        """ This method prints out the bytes as they are received.
        
            This method must be implemented by any class wishing to be a
            LoopbackHandler.  The parameter received is an integer value
            of the byte that was received by the serial port.
        """
        print(intByte)


class LoggingLoopbackHandler(object):
    """ A loopback handler that prints each byte received to the specified
        log file.
    """
    
    def __init__(self, filename="loopback_log.txt"):
        """ Constructs a LoggingLoopbackHandler.
        
            Params:
            filename    The name of the log file, if not specified it 
                        defaults to "loopback_log.txt".
        """
        self.__filename = filename
    
    def handleByte(self, intByte):
        """ This method logs the bytes to the specified logfile.
        
            This method must be implemented by any class wishing to be a
            LoopbackHandler.  The parameter received is an integer value
            of the byte that was received by the serial port.
        """
        with open(self.__filename, 'a') as logFile:
            logFile.write(str(intByte) + "\n")
