"""
CircuitPython library for the MCP23S17 SPI I/O expander.
"""

import board
import busio
import digitalio
import MCP23S17

class expander:

    # Constructor for the class.  "address" is the default address for the SPI chip
    # Change it if you set pins A0-A2
    def __init__(self, SCK, MISO, MOSI, CS, address = 0b01000000):

        # Set up the Chip Select pin
        self.cs = digitalio.DigitalInOut(CS)
        self.cs.direction = digitalio.Direction.OUTPUT
        self.cs.value = True
        self.cs.value = False
        self.cs.value = True

        # Set up the SPI bus
        self.spi = busio.SPI(SCK, MISO=MISO, MOSI=MOSI)

        # Set the initial SPI configuration
        while not self.spi.try_lock():
            pass
        self.spi.configure(baudrate=5000000, phase=0, polarity=0)
        self.spi.unlock()

        # Addresses for SPI read/writes
        self.writeAddress = address
        # Read address is write + 1
        self.readAddress = address | 0b1

    # Generic internal function to write to the chip
    def _write(self, register, data):

        # Wait until the SPI bus is locked
        while not self.spi.try_lock():
            pass

        # Re-set the SPI config
        self.spi.configure(baudrate=5000000, phase=0, polarity=0)
        # Select the MCP23S17
        self.cs.value = False
        # Write the writeAddress byte, register, and then the byte to write
        self.spi.write(bytearray([self.writeAddress, register] + data))
        # Unselect the chip
        self.cs.value = True

        # Unlock the bus
        self.spi.unlock()

    # Generic internal function to read from the chip
    def _read(self, register, numBytes):

        # An array to read data into 
        readData = bytearray(numBytes)

        # Wait until the SPI bus is locked
        while not self.spi.try_lock():
            pass

        # Select the chip
        self.cs.value = False
        # Re-set the SPI config
        self.spi.configure(baudrate=5000000, phase=0, polarity=0)
        # Write the readAddress byte, and the register to read
        self.spi.write(bytearray([self.readAddress, register]))
        # Read data into readData
        self.spi.readinto(readData)
        #Unselect the MCP23S17
        self.cs.value = True
        # Unlock the SPI bus
        self.spi.unlock()

        return(list(readData))

    """
    Function to set the direction of pins. "bank" should be "A" or "B", 
    pin should EITHER be an int (0-7)  OR a list of these ints ([0,1,2] etc.).
    Refer to the chip pinout.  "direction" shoud be "output" or "input".
    """
    def dir(self, bank, pin, direction):

        try:
            if (bank.lower() != "a") and (bank.lower() != "b"):
                print("Error, bank must be 'a' or 'b'.")
                return
            else:
                if bank.lower() == "a":
                    register = 0x00
                elif bank.lower() == "b":
                    register = 0x01

        except AttributeError:
            print("Error, bank must be 'a' or 'b'.")
            return

        if isinstance(pin, int):
            if not (pin >= 0) and (pin <= 7):
                print("Error, pin must be 0-7.")
                return
        elif isinstance(pin, list):
            for eachPin in pin:
                if not (eachPin >= 0) and (eachPin <= 7):
                    print("Error, pin must be 0-7.")
                    return
        else:
            print("Error, pin must be an int or list.")
            return

        if (direction.lower() != "output") and\
                (direction.lower() != "input"):
            print("Error, mode must be 'input' or 'output'.")

        currentValue = self._read(register, 1)[0]

        # bit goes low
        if direction == "output":
            if isinstance(pin, int):
                currentValue = currentValue & (0xff - (1 << pin))
            else:
                for eachPin in pin:
                    currentValue = currentValue & (255 - (1 << eachPin))
        # Bit goes high
        else:
            if isinstance(pin, int):
                currentValue |= 1 << pin
            else:
                for eachPin in pin:
                    currentValue |= 1 << eachPin

        # Write the new value back
        self._write(register, [currentValue])

    
    """
    Function to set the value of output pins.  "bank" should be "A"
    or "B", pin should EITHER be an int (0-7) or a list of these ints
    ([0,1,2] etc.), refer to the pinout.  "state" should be True (pin high)
    or False (Pin low).
    """
    def value(self, bank, pin, state):

        try:
            if (bank.lower() != "a") and (bank.lower() != "b"):
                print("Error, bank must be 'a' or 'b'.")
                return
            else:
                if bank.lower() == "a":
                    register = 0x14
                elif bank.lower() == "b":
                    register = 0x15

        except AttributeError:
            print("Error, bank must be 'a' or 'b'.")
            return

        if isinstance(pin, int):
            if not (pin >= 0) and (pin <= 7):
                print("Error, pin must be 0-7.")
                return
        elif isinstance(pin, list):
            for eachPin in pin:
                if not (eachPin >= 0) and (eachPin <= 7):
                    print("Error, pin must be 0-7.")
                    return
        else:
            print("Error, pin must be an int or list.")
            return

        if (state != True) and (state != False):
            print("Error, mode must be 'True' or 'False'.")

        # Point to the current port register
        #self._write(register, [])
        # Read the current value
        currentValue = self._read(register, 1)[0]

        # bit goes low
        if state == False:
            if isinstance(pin, int):
                currentValue = currentValue & (0xff - (1 << pin))
            else:
                for eachPin in pin:
                    currentValue = currentValue & (255 - (1 << eachPin))
        # Bit goes high
        else:
            if isinstance(pin, int):
                currentValue |= 1 << pin
            else:
                for eachPin in pin:
                    currentValue |= 1 << eachPin

        # Write the new value back
        self._write(register, [currentValue])


    """
    Read and return an entire bank (A or B) as a single 8-bit int.
    Bank should be "A" or "B".
    """
    def readBank(self, bank):

        try:
            if (bank.lower() != "a") and (bank.lower() != "b"):
                print("Error, bank must be 'a' or 'b'.")
                return
            else:
                if bank.lower() == "a":
                    register = 0x12
                elif bank.lower() == "b":
                    register = 0x13

        except AttributeError:
            print("Error, bank must be 'a' or 'b'.")
            return

        currentValue = self._read(register, 1)

        return(currentValue[0])
        
    
    """
    Read and return a single pin only.  "pin" should be "An" or "Bn"
    where A/B refers to the bank, and n refers to the pin number.
    """
    def readPin(self, pin):

        bank = pin[0]
        pin = int(pin[1])
        
        try:
            if (bank.lower() != "a") and (bank.lower() != "b"):
                print("Error, bank must be 'a' or 'b'.")
                return
            else:
                if bank.lower() == "a":
                    register = 0x12
                elif bank.lower() == "b":
                    register = 0x13

        except AttributeError:
            print("Error, bank must be 'a' or 'b'.")
            return
        
        if not ((pin >= 0) and (pin <= 7)):
            print("Error, pin must be 0-7.")
            return

        currentValue = self._read(register, 1)
        

        return((currentValue[0] >> pin) & 0b1)


    """
    Set the pullup resistor on pins.  "bank" should be "A" or "B", 
    pin should EITHER be an int (0-7) or a list of ints ([0,1,2] etc.), 
    refer to the pinout.  "mode" should be "up" (pullup is active) or
    "none" (no pullup on that pin).
    """
    def pullup(self, bank, pin, mode):

        try:
            if (bank.lower() != "a") and (bank.lower() != "b"):
                print("Error, bank must be 'a' or 'b'.")
                return
            else:
                if bank.lower() == "a":
                    register = 0x0C
                elif bank.lower() == "b":
                    register = 0x0D

        except AttributeError:
            print("Error, bank must be 'a' or 'b'.")
            return

        if isinstance(pin, int):
            if not (pin >= 0) and (pin <= 7):
                print("Error, pin must be 0-7.")
                return
        elif isinstance(pin, list):
            for eachPin in pin:
                if not (eachPin >= 0) and (eachPin <= 7):
                    print("Error, pin must be 0-7.")
                    return
        else:
            print("Error, pin must be an int or list.")
            return

        if (mode.lower() != "up") and\
                (mode.lower() != "none"):
            print("Error, mode must be 'up' or 'none'.")

        currentValue = self._read(register, 1)[0]

        # bit goes low
        if mode == "none":
            if isinstance(pin, int):
                currentValue = currentValue & (0xff - (1 << pin))
            else:
                for eachPin in pin:
                    currentValue = currentValue & (255 - (1 << eachPin))
        # Bit goes high
        else:
            if isinstance(pin, int):
                currentValue |= 1 << pin
            else:
                for eachPin in pin:
                    currentValue |= 1 << eachPin

        # Write the new value back
        self._write(register, [currentValue])
