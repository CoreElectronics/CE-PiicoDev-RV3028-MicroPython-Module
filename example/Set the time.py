# set the date and time

from PiicoDev_RV3028 import *

date = {
    'year'  : 21,
    'month' : 12,
    'day'   : 3
}
time = {
    'hour'  : 9,
    'min'   : 38,
    'sec'   : 0
}

rtc = PiicoDev_RV3028()

rtc.setDate(date)
rtc.setTime(time)

print('Time set to: ', end='')
print(rtc.timestamp())