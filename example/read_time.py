# A simple example to read the date, timestamp and weekday from the PiicoDev RTC
from PiicoDev_RV3028 import *
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028()

while True:
    print(rtc.timestamp())
    sleep_ms(1000)