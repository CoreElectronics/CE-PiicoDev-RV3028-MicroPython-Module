# A simple example to read the date, timestamp and weekday from the PiicoDev RTC
from PiicoDev_RV3028 import *

rtc = PiicoDev_RV3028()

while True:
    print(rtc.timestamp())
    print(rtc.weekday)
    sleep_ms(1000)