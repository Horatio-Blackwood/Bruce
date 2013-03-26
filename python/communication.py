# Adam Anderson
# February 12, 2012
#
# Protocol Defintition:
#
# MOUSE PACKET
# [Header] [P1] [P2] [P3] [FOOTER]
# [130]    [  ] [  ] [  ] [134]
#       P1:  -64 to 64 amount of X-Movement. (Signed)
#       P2:  -64 to 64 amount of Y-Movement. (Signed)
#
#       P3:  0 = No Click, 
#            1 = Left Click 
#            2 = Right Click
#            3 = Left Press
#            4 = Right Press
#            5 = Left Release
#            6 = Right Release
#            All others inputs are ignored, (treated as no click)
# 
# KEYBOARD PACKET
# [Header] [P1] [P2] [P3] [FOOTER]
# [131]    [  ] [  ] [  ] [134]
#
#       P1:  Key Value ['a' - 'Z' etc.....]
#       P2:  0 = Press
#            1 = Release
#            2 = Click
#       P3:  RESERVED (Future use as a modifier key?)
#
# READY PACKET - From Arduino to Python PC.
# [132] - Ready
# [133] - Not Ready


from commands import KeyPushType
from commands import KeyPressDescriptor
from commands import ClickDescriptor

# Header Byte for a Click Message.
CLICK_HEADER = 130

# Header Byte for a Key Message.
KEY_HEADER = 131

# Footer byte for _ANY_ Message.
FOOTER = 134

def buildMouseCommand(clickDescriptor=ClickDescriptor(), xMove=0, yMove=0):
    """ Constructs the bytes to send on the serial port to send a mouse
        Command, and returns it as a List of Bytes.
        
        clickDescriptor     - A clickDescriptor that defines a click.  The
                              default descriptor is a no-click descriptor.
        
        xMove               - the x-move value.  Max value is 64, min 
                              value is -64.
                              
        yMove               - the y-move value.  Max value is 64, min 
                              value is -64.
    """
    if clickDescriptor == None:
        raise ValueError("Parameter 'clickDescriptor' must not be None.")
        
    if xMove == None or yMove == None:
        raise ValueError("xMove and yMove must not be None")
        
    if xMove > 64 or yMove > 64 or xMove < -64 or yMove < -64:
        raise ValueError("xMove and yMove must be between -64 and 64 (inclusive).")
        
    messageBytes = []
    messageBytes.append(CLICK_HEADER.to_bytes(1, byteorder='little'))
    messageBytes.append(xMove.to_bytes(1, byteorder='little', signed=True))
    messageBytes.append(yMove.to_bytes(1, byteorder='little', signed=True))
    messageBytes.append(clickDescriptor.getByte())
    messageBytes.append(FOOTER.to_bytes(1, byteorder='little'))
    
    return messageBytes
    
    
    
def buildKeyboardCommand(keyPressDescriptor):
    """ Constructs and returns a List of bytes that represent a fully
        formed keyboard packet.
    """
    if keyPressDescriptor == None:
        raise ValueError("keyPressDescriptor must not be None.")
    
    keyPressDescriptor
    
    messageBytes = []
    messageBytes.append(KEY_HEADER.to_bytes(1, byteorder='little'))
    messageBytes.append(keyPressDescriptor.getKeyByte())
    messageBytes.append(keyPressDescriptor.getPushTypeByte())
    messageBytes.append((0).to_bytes(1, byteorder='little'))
    messageBytes.append(FOOTER.to_bytes(1, byteorder='little'))
    
    return messageBytes
    
    
def buildKeyPhraseCommands(text):
    """ Takes a String and returns a List of packets (a List of Lists of bytes)
        to be sent over serial.
        
        text    - the String to send in successive packets (one character
                  per packet) via the Serial port.
    """
    if text == None:
        return
        
    if (len(text) == 0):
        return
    
    packets = []
    for each in text:
        packets.append(buildKeyboardCommand(KeyPressDescriptor(each, KeyPushType.CLICK)))
        
    return packets
