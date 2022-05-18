# PiicoDev Real Time Clock RV-3028
# Some examples of how to set an alarm
# Alarms can trigger on a combination of minutes, hours, and weekday/date

from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms
rtc = PiicoDev_RV3028() # Initialise the RTC module (24-hr mode by default), enable charging

### Trigger once per hour, at the start of the hour
rtc.alarmSetup(minutes=4) # Triggers once when the minutes match

### Trigger once per week on Wednesday (day 2) at 1:23 PM
# rtc.alarmSetup(weekday=2, hours=13, minutes=23) # Trigger once per week at the scheduled day and time

while True:
    print(rtc.timestamp())
    if rtc.checkAlarm():
        print("Alarm Triggered")
        
    sleep_ms(1000)
