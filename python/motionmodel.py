# Adam Anderson
# February 25, 2013

from fractions import Fraction
from math import floor
from math import fabs
from communication import buildMouseCommand
from commands import ClickDescriptor

# The maximum allowable denominator - used to reduce fractions to manageable values.
MAX_DENOMINATOR = 8

MOVE_CHUNK = 2

class MotionModel(object):
    """ A class that represents a MotionModel.  MotionModels use their
        getPath() method to calculate a List of packets (Lists of bytes)
        that describe the mouse's motion from one point to another.
    """        
    
    def getPath(self, xMove, yMove):
        """ Generates a List of Packets (lists of bytes) that describe
            the mouse's motions from the current mouse position to the 
            relative position described by the xMove and yMove values.
            
            xMove   - Integer.  the amount of x to move 
        """
        raise NotImplementedError("Sub-classes must implement this method.")


class SimpleMotionModel(MotionModel):
    """ A motion model that calculates a direct, straight line path 
        from the current mouse position to the destination using the 
        getPath() method.
    """
    
    def __init__(self):
        """ Creates a new instance of Simple motion model.
        """
        super(SimpleMotionModel, self).__init__()
        
    
    def getPath(self, xMove, yMove):
        """ Returns a List of packets (a packet being a List of Bytes)
            that represent a series of moves to create a path from the 
            current position to the relative point specified by the xMove
            and yMove parameters.
            
            xMove       - An Integer value that represents the relative
                          x position to move the mouse to.
                          
            yMove       - An Integer value that represents the relative
                          y position to move the mouse to.
        """

        # Initialize the packet List to send back.
        packets = []
        
        # If both moves are zero, return an empty List - there is 
        # nowhere to go.
        if xMove == 0 and yMove == 0:
            return packets

        # if the x-move is zero, chunk up the vertical movements into 
        # lengths of 2.
        if xMove == 0:
            absoluteYMove = abs(yMove)
            moveCount = floor(absoluteYMove / MOVE_CHUNK)
            
            print("MC", moveCount)
            
            if (yMove < 0):
                chunk = -1 * MOVE_CHUNK
            else:
                chunk = MOVE_CHUNK
            
            print("C", chunk)
            
            
            for i in range(moveCount):
                packets.append(buildMouseCommand(ClickDescriptor(), 0, chunk))
                
            remainder_y = yMove % MOVE_CHUNK
            if chunk * remainder_y < 0:
                remainder_y = remainder_y * -1
                
            print("R", remainder_y)
            packets.append(buildMouseCommand(ClickDescriptor(), 0, remainder_y))
            print("\n end")
            
            return packets
            
        else:
            # Figure out the Slope of the line from the current position, 
            # (0,0) to the specified X and Y position.
            slope = Fraction(yMove, xMove)
            slope = slope.limit_denominator(MAX_DENOMINATOR)
            
            x_chunk = slope.denominator
            if xMove * x_chunk < 0:
                x_chunk = x_chunk * -1
              
            y_chunk = slope.numerator
            if yMove * y_chunk < 0:
                y_chunk = y_chunk * -1
            
            # Calculate the number of "whole" moves that need to be made
            moveCount = abs(floor(xMove / slope.denominator))
            
            # Build and add all of the "whole moves".
            for i in range(moveCount):
                packets.append(buildMouseCommand(ClickDescriptor(), x_chunk, y_chunk))

            # build and append the fractional, "partial" move to put us in the right
            # final position.
            remainder_x = xMove % slope.denominator
            if remainder_x * slope.denominator < 0:
                remainder_x = remainder_x * -1

            if slope.numerator == 0:
                remainder_y = 0
            else:
                remainder_y = yMove % slope.numerator
                if remainder_y * slope.numerator < 0:
                    remainder_y = remainder_y * -1
            
            packets.append(buildMouseCommand(ClickDescriptor(), remainder_x, remainder_y))
            return packets
