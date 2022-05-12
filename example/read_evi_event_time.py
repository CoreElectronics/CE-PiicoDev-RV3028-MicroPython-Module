# Read the EVI pin event time.
# The program will continue listening for an event until one is detected.
from PiicoDev_RV3028 import PiicoDev_RV3028
from PiicoDev_Unified import sleep_ms

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
