# Read the EVI pin event time

from PiicoDev_RV3028 import *

rtc = PiicoDev_RV3028()

rtc.resetEventInterrupt(edge = 'falling')

while (rtc.getEventInterrupt() is False):
    print('Checking is there has been a falling edge on EVI pin')
    sleep_ms(10000)
print('Event occurred at the exact time: ', end='')
print(rtc.getDateTime(eventTimestamp=True))
    
