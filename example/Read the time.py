# read the date and time

from PiicoDev_RV3028 import *

rtc = PiicoDev_RV3028()

while True:
    print(rtc.timestamp())
    sleep_ms(1000)