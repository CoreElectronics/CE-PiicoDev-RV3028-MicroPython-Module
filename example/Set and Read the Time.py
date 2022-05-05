# PiicoDev Real Time Clock RV-3028
# An example of how to set and read the date, time, and weekday

from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

rtc = PiicoDev_RV3028() # Initialise the RTC module, enable charging

# Set the time by assigning values to rtc's attributes
rtc.day = 4
rtc.month = 5
rtc.year = 2022
rtc.hour = 13
rtc.minute = 41
rtc.second = 00
rtc.ampm = '24' # 'AM','PM' or '24'. Defaults to 24-hr time
rtc.weekday = 'wednesday' # Rolls over at midnight, works independently of the calendar date
rtc.setDateTime() # Sets the time with the above values

# Get the current time
rtc.getDateTime()

# Print the current time, and today's name
# You can read from individual time attributes eg hour, minute, weekday.
print('The time is ' + str(rtc.hour) + ":" + str(rtc.minute))
print('Today is: ' + str(rtc.weekday))

while True:
    print(rtc.timestamp()) # timestamp() returns a pre-formatted string. Useful for printing and datalogging!
    sleep_ms(1000)