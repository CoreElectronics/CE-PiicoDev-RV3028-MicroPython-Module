from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028() # Initialise the RTC module

print(rtc.getUnixTime())
rtc.setUnixTime(0)
print(rtc.getUnixTime())