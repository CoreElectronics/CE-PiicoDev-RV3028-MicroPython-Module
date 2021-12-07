from PiicoDev_RV3028 import PiicoDev_RV3028
rtc = PiicoDev_RV3028()
print()
print('Timestamp:')
print(rtc.timestamp())
print()

# Interrupts
rtc.clearAllInterrupts()
rtc.resetEventInterrupt()

while rtc.getEventInterrupt() is False:
    sleep_ms(100)
    continue

print(rtc.getDateTime(timeFormat = 'dict', eventTimestamp = True))