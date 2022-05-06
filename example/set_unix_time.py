from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028() # Initialise the RTC module
rtc.setUnixTime(0) # reset UNIX time

while True:
    print(rtc.getUnixTime()) # display UNIX time
    sleep_ms(1500)