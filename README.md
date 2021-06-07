# CircuitPython_MCP23S17
Module for driving an MCP23S17 using CircuitPython

This was written and tested on a Feather M4 Express running CircuitPython 6.2.0.

To use this, copy MCP23S17.py into your CircuitPython device (either to the root or into the `lib` folder), and then set up and run the chip.  An example of how to do this is in `example.py`.

Currently working:
* Setting pins as inputs/outputs, either individually or in groups
* Setting and clearing pull up resistors, either individually or in groups
* Reading input pins, individually or in groups
* Setting output pins high or low, individually or in groups

Currently not working:
* Anything else (interrupts, IOCON.SEQOP etc.)

Needs done:
* Interrupts
* Reading pins could probably be rolled into a single function for reading single or groups of pins, as the other functions are

# The class

`expander = MCP23S17(SCK, MISO, MOSI, CS, address = 0b01000000)`

`SCK`, `MISO`, `MOSI` should probably be the corresponding SPI pins on your board.  `CS` can be any digital pin, as long as it is hooked up as the chip select for the MCP23S17.  `address` is, by default, the address when pins A0-2 are floating, but can be changed if you want to (yes, this SPI device has a read/write address, I've no idea why).

# Functions

## dir

`dir(bank, pin, direction):`

Function to set the direction of pins. "bank" should be "A" or "B", pin should EITHER be an int (0-7) to set a single pin, OR a list of these ints to set many from *the same bank* at the same time ([0,1,2] etc.).  Refer to the chip pinout: these correspond to GPA0-7 and GPB0-7.  "direction" shoud be "output" or "input".

## value

`value(bank, pin, state)`
    
Function to set the value of output pins.  "bank" should be "A" or "B", pin should EITHER be an int (0-7) to set a single pin, or a list of these ints to set many from *the same bank* at the same time ([0,1,2] etc.), refer to the pinout: these correspond to GPA0-7 and GPB0-7.  "state" should be True (pin high) or False (Pin low).

## readBank
`readBank(bank):`

Read and return an entire bank (A or B) as a single 8-bit int.  Bank should be "A" or "B".  Bit 0 refers to pin 0, bit 1 to pin 1 etc..

## readPin

`readPin(pin)`

Read and return a single pin only.  "pin" should be "An" or "Bn" where A/B refers to the bank, and n refers to the pin number.  Returns an int of 1 if the pin is high, or 0 if the pin is low.  As per the notes at the beginning, `readPin` and `readBank` probably need rejigged into a single function.

## pullup

`pullup(bank, pin, mode)`

Set the pullup resistor on pins.  "bank" should be "A" or "B", pin should EITHER be an int (0-7) to set a single pin, or a list of ints to set many from *the same bank* at the same time ([0,1,2] etc.), refer to the pinout: these correspond to GPA0-7 and GPB0-7.  "mode" should be "up" (pullup is active) or "none" (no pullup on that pin).
