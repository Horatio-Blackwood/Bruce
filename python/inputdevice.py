# Adam Anderson
# February 24, 2013

from commands import *
from motionmodel import SimpleMotionModel
import communication


class Mouse(object):
    """ A non-thread-safe object that represents a hardware Mouse.  This
        class models a Mouse object that sends messages via the provided
        serial port object.
    """
    
    def __init__(self, serialPort, motionModel=SimpleMotionModel()):
        """ Constructor.  Creates a Mouse object with the supplied 
            SerialPort from the serialport module.
            
            serialPort  - The serial port to send the mouse commands via.
                          If None/Null is provided, a ValueError is raised.
        """
        if serialPort == None:
            raise ValueError("Parameter 'serialPort' cannot be 'None.'")
            
        if motionModel == None:
            raise ValueError("Parameter 'motionModel' cannot be 'None.'")
        
        self.__serialPort = serialPort
        self.__motionModel = motionModel
        
        self.doClick(MouseButton.LEFT, ClickType.RELEASE)
        self.doClick(MouseButton.RIGHT, ClickType.RELEASE)
            
        # Initialize location - The starting position of the mouse is 
        # the 'origin' of the grid upon which the mouse moves.
        self.__x = 0
        self.__y = 0
        
        
    
    def doLeftClick(self):
        """ Performs a left click in the Mouse's current location.
        """
        # Send a single left click via serial with no 
        self.doClick(MouseButton.LEFT, ClickType.CLICK)
        
    
    def doRightClick(self):
        """ Performs a Right click in the Mouse's current location.
        """
        # Send a single right click via serial with no 
        self.doClick(MouseButton.RIGHT, ClickType.CLICK)
        
    
    def doClick(self, button=MouseButton.LEFT, clickType=ClickType.CLICK):
        """ Performs a click as specified by the button and click type in the
            parameters.
            
            Params:
            button      the button to click.
            clickType   the type of click to perform.
        """
        packet = communication.buildMouseCommand(ClickDescriptor(button, clickType), 0, 0)
        self.__serialPort.sendBytes(packet)
        
    
    def move(self, xMove, yMove):
        """ Performs a relative move from the mouse's current position.
            When completed, this mouse object will have moved the provided
            xMove value along the x-axis and the yMove value along the 
            y-axis.
            
            xMove   - the amount of X coordinate movement.
                      
            yMove   - the amount of Y coordinate movement.
        """
            
        # Builds the 
        for packet in self.__motionModel.getPath(xMove, yMove):
            self.__serialPort.sendBytes(packet)
        
        # update location.
        self.__x += xMove
        self.__y += yMove
        
        
    def doClickDragRelease(self, xMove, yMove, mouseButton=MouseButton.LEFT):
        """ Performs a click, drag, release operation from the mouse's
            current location 
            
            mouseButton - the button to click and drag with, (as specified
                          in the MouseButton class in the commands module.
                          If not specified, this method defaults to the 
                          Left mouse button.
            
            xMove       - the amount of X coordinate movement.
                      
            yMove       - the amount of Y coordinate movement.
        """
        if mouseButton == None:
            raise ValueError("mouseButton must not be None.")
        
        packets = []
        packets.append(communication.buildMouseCommand(ClickDescriptor(mouseButton, ClickType.PRESS), 0, 0))
        packets = packets + self.__motionModel.getPath(xMove, yMove)
        packets.append(communication.buildMouseCommand(ClickDescriptor(mouseButton, ClickType.RELEASE), 0, 0))
        
        for packet in packets:
            self.__serialPort.sendBytes(packet)
        
        # update location.
        self.__x += xMove
        self.__y += yMove

    
    def returnToOrigin(self):
        """ Returns the mouse position to its original position.
        """
        x = (-1 * self.__x)
        y = (-1 * self.__y)
        for packet in self.__motionModel.getPath(x, y):
            self.__serialPort.sendBytes(packet)
            
        self.__x += x
        self.__y += y
        
        
    def getLocation(self):
        """ Returns the x and y values (respectively) of this Mouse object's
            current position relative to its original position, (the 
            position the mouse cursor was when the script was started).
        """
        return self.__x, self.__y



class Keyboard(object):
    """ An object that model a hardware Keyboard in order to send 
        keystrokes in an automated fashion.
    """
    
    def __init__(self, serialPort):
        """ Constructor, creates a new instance of Keyboard.
        """
        self.__serialPort = serialPort
        
    def typeKey(self, character, keyPushType=KeyPushType.CLICK):
        """ Sends a single key-press as described by the provided KeyPressDescriptor.
        """
        packet = communication.buildKeyboardCommand(KeyPressDescriptor(character, keyPushType))
        self.__serialPort.sendBytes(packet)
    
    def typeKeyPhrase(self, text):
        """
        """
        # Get a List of Lists of Bytes
        packets = communication.buildKeyPhraseCommands(text)
        
        # for each list of bytes, call send.
        for packet in packets:
            self.__serialPort.sendBytes(packet)
