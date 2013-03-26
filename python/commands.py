# Adam Anderson
# February 12, 2012

class MouseButton(object):
    """ An enumeration of mouse buttons that can be clicked.
    """
    NO_BUTTON = "no_button"
    LEFT = "left"
    RIGHT = "right"
    MIDDLE = "middle"
    
    
class ClickType(object):
    """ An enumeration of Click Types.
    """
    NO_CLICK = "no_click"
    CLICK = "click"
    PRESS = "press"
    RELEASE = "release"
    
class KeyPushType(object):
    """ An enumeration of Key Push Types.
    """
    PRESS = "press"
    RELEASE = "release"
    CLICK = "click"
    
class ClickDescriptor(object):
    """ An object that defines a click.  This includes both the button 
        used for the click and the type of click action that is to be
        taken by clicks described by this descriptor object. 
    """
    
    def __init__(self, button=MouseButton.NO_BUTTON, clicktype=ClickType.NO_CLICK):
        """ Constructs a new ClickDescriptor.
        
            button      - A MouseButton, must not be null/None.  Default is NO_BUTTON if
                          nothing is specified.
                          
            clickType   - A ClickType, must not be null/None.  Default is NO_CLICK if 
                          nothing is specified.
        """         
        self.__button = button
        self.__click = clicktype
        
    def getByte(self):
        """ Returns a single byte that represents the click descriptor 
        """
        if (self.__button == MouseButton.LEFT and self.__click == ClickType.CLICK):
            return (1).to_bytes(1, byteorder='little')
            
        if (self.__button == MouseButton.RIGHT and self.__click == ClickType.CLICK):
            return (2).to_bytes(1, byteorder='little')
        
        if (self.__button == MouseButton.LEFT and self.__click == ClickType.PRESS):
            return (3).to_bytes(1, byteorder='little')
            
        if (self.__button == MouseButton.RIGHT and self.__click == ClickType.PRESS):
            return (4).to_bytes(1, byteorder='little')
            
        if (self.__button == MouseButton.LEFT and self.__click == ClickType.RELEASE):
            return (5).to_bytes(1, byteorder='little')
            
        if (self.__button == MouseButton.RIGHT and self.__click == ClickType.RELEASE):
            return (6).to_bytes(1, byteorder='little')
            
        return (0).to_bytes(1, byteorder='little')
        
            
class KeyPressDescriptor(object):
    
    def __init__(self, character, keyPushType=KeyPushType.CLICK):
        """ Constructs a new KeyPressDescriptor.
        
            character:      The Character to send as a 'char' object.
            keyPushType:    The KeyPushType of the key push (PRESS or RELEASE)
        """
        
        if (character == None):
            raise ValueError("Parameter 'character' cannot be None")
            
        if (len(character) > 1 or len(character) < 1):
            raise ValueError("Parameter 'character' must be a single character.")
            
        if (keyPushType == None):
            raise ValueError("Parameter 'keyPushType' cannot be None.")
        
        self.__char = character
        self.__keyPushType = keyPushType
        
        
    def getKeyByte(self):
        """ Returns the byte that represents the Key this packet is 
            assembled for.
        """
        return (self.__char).encode()
        
    
    def getPushTypeByte(self):
        """
        """
        if self.__keyPushType == KeyPushType.PRESS:
            return (0).to_bytes(1, byteorder='little')
            
        if self.__keyPushType == KeyPushType.RELEASE:
            return (1).to_bytes(1, byteorder='little')

        if self.__keyPushType == KeyPushType.CLICK:
            return (2).to_bytes(1, byteorder='little')
