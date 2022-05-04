from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028() # Initialise the RTC module

# Show current RTC time, untampered with
rtc.getDateTime()
print(rtc.timestamp())

# Setting the time
rtc.day = 4
rtc.month = 5
rtc.year = 2022
rtc.hour = 13
rtc.minute = 41
rtc.second = 00
rtc.ampm = '24' # 'AM','PM' or '24'. Defaults to 24-hr time
rtc.weekday = 'Wednesday' # Rolls over at midnight, works independently of the calendar date.
rtc.setDateTime()

sleep_ms(3000)

# Get the current time
rtc.getDateTime()
print(rtc.timestamp())
print('Day of week: ' + str(rtc.weekday))