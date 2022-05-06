# Read the EVI pin event time

from PiicoDev_RV3028 import *

rtc = PiicoDev_RV3028()

rtc.resetEventInterrupt(edge = 'falling')

rtc.getDateTime()
print('Monitoring started at: ' + rtc.timestamp())

while (rtc.getEventInterrupt() is False):
    print('Waiting for 10 seconds.  If there is a falling edge on EVI pin the time will be recorded.')
    sleep_ms(10000)
print('Event occurred at: ', end='')
rtc.getDateTime(eventTimestamp=True)
print(rtc.timestamp(eventTimestamp=True))
    
