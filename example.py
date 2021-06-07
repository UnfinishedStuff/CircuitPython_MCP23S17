"""
Demo script for the MCP23S17 driven by CircuitPython
Connect LEDs to all pins on Bank B
Connect an LED to pin A7, with the other side grounded

The odd and even LEDs should blink alternately.
The script should continuously print "1" for pin A7
(as the pull-up resistor is set), but print "0"
when the button is pressed.
"""

import board
import busio
import digitalio
import time
import MCP23S17

# Set up the Class
chip = MCP23S17.expander(board.SCK,
                            board.MISO,
                            board.MOSI,
                            CS=board.D4)

# Set all pins on bank B to be outputs
chip.dir("b", [0, 1, 2, 3, 4, 5, 6, 7], "output")
# Set pin A7 to have a pullup resistor
chip.pullup("a", 7, "up")
# Set pin A7 to be an input
chip.dir("a", 7, "input")

# Do this forever:
while True:
    # Set odd-numbered bank B LEDs high
    chip.value("b", [1, 3, 5, 7], True)
    # Set even-numbered bank B LEDs low
    chip.value("b", [0, 2, 4, 6], False)
    # Print the current state of pin A7
    print(chip.readPin("a7"))
    time.sleep(0.5)
    
    # Set odd-numbered bank B LEDs low
    chip.value("b", [1, 3, 5, 7], False)
    # Set even-numbered bank B LEDs high
    chip.value("b", [0, 2, 4, 6], True)
    # Print the current state of pin A7
    print(chip.readPin("a7"))
    time.sleep(0.5)
