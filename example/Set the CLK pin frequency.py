# Set the CLK output pin frequency

from PiicoDev_RV3028 import *

clk = 32768 # The frequency, in Hz, of the square wave on the CLK output pin. Valid values are: 32768, 8192, 1024, 64, 32, 1, and 0 (always low).

rtc = PiicoDev_RV3028()

rtc.configClockOutput()
