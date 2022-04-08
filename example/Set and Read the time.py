from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028() # Initialise the RTC module

# Setting the time
rtc.getDateTime()
print(rtc.timestamp())

rtc.day = 8
rtc.month = 4
rtc.year = 22
rtc.hour = 11
rtc.minute = 59
rtc.second = 58
rtc.ampm = 'PM' # 'AM','PM' or '24'. Defaults to 24-hr time
rtc.setDateTime()

sleep_ms(3000)

# Get the current time
rtc.getDateTime()
print(rtc.timestamp())