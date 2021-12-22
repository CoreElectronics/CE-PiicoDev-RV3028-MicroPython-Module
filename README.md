<!-- TODO How to use this template
Follow these commented instructions to build the repo.
Delete the instructions as you go, to keep for a cleaner final file.
 -->

<!-- TODO Initialise the repo with the following two files:
 The MicroPython Module for this device with name: "PiicoDev_[DEVICE MFN].py". Eg for temperature sensor TMP117: PiicoDev_TMP117.py
 A (tested) main.py file
-->


<!-- TODO update title to be descriptive. Eg.
PiicoDev® [Description] [Part#] MicroPython Module
PiicoDev® Precision Temperature Sensor TMP117 MicroPython Module -->
# PiicoDev® Template MicroPython Module

<!-- TODO update link URL with CE SKU -->
<!-- TODO update link title -->
This is the firmware repo for the [Core Electronics PiicoDev® XXXXXX](https://core-electronics.com.au/catalog/product/view/sku/XXXXXX)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

<!-- TODO update tutorial link with the device tinyurl eg. piico.dev/p1
See the [Quickstart Guide](https://piico.dev/pX)
 -->

<!-- TODO verify the tested-devices list -->
This module has been tested on:
 - Micro:bit v2
 - Raspberry Pi Pico
 - Raspberry Pi SBC

## Details

This module only implements a subset of the RV3028's features. A full register map can be found in the RV-3028-C7 Application Manual: https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3028-C7_App-Manual.pdf

### `PiicoDev_RV3028(bus=, freq=, sda=, scl=, addr=0x52)`
Parameter | Type | Range            | Default                               | Description
--------- | ---- | ---------------- | ------------------------------------- | --------------------------------------------------
bus       | int  | 0, 1             | Raspberry Pi Pico: 0, Raspberry Pi: 1 | I2C Bus.  Ignored on Micro:bit
freq      | int  | 100-1000000      | Device dependent                      | I2C Bus frequency (Hz).  Ignored on Raspberry Pi
sda       | Pin  | Device Dependent | Device Dependent                      | I2C SDA Pin. Implemented on Raspberry Pi Pico only
scl       | Pin  | Device Dependent | Device Dependent                      | I2C SCL Pin. Implemented on Raspberry Pi Pico only
addr      | int  | 0x52             | 0x52                                  | This address cannot be changed

### getUnixTime()

Returns the current UNIX time in the RV3028. Note that this is not converted to "correct" UNIX time and is simply an integer equal to the number of seconds since reset (or call to `setUnixTime()`).

### setUnixTime(time)

Parameter | Type | Default | Description
--- | --- | --- | ---
time | Integer | None | The UNIX time to load into the RV3028's UNIX time registers. These registers hold a 32-bit integer which increments once per second.

### setBatterySwitchover(state = True)

Sets the battery switchover to direct switching mode (switchover when Vdd < Vbackup). This method is called in __init__() so that the EEPROM state doesn't need to be trusted.

Parameter | Type | Default | Description
--- | --- | --- | ---
state | Boolean | True | If True the battery switchover mode is set to direct switching mode. If False battery switchover is disabled.

### setTrickleCharger(state = True)

Enables the tricker charger. This is required to charge the onboard supercapacitor.

See also: `configTrickleCharger()`

Parameter | Type | Default | Description
--- | --- | --- | ---
state | Boolean | True | If True the trickle charger is enabled. If False the trickle charger is disabled.

### configTrickleCharger(R = '3k')

Selects one of four different internal trickle charger resistors. This resistor is placed in series with a Schottky diode between Vcc and the supercap's + terminal.

Parameter | Type | Default | Description
--- | --- | --- | ---
R | String | '3k' | The trickle charger resistor is set to the value described by this string. Valid values are '3k', '5k', '9k', and '15k'.

### configClockOutput(clk = 32768)

Sets the frequency of the CLK output pin.

Parameter | Type | Default | Description
--- | --- | --- | ---
clk | Integer | 32768 | The frequency, in Hz, of the square wave on the CLK output pin. Valid values are: 32768, 8192, 1024, 64, 32, 1, and 0 (always low).

### resetEventInterrupt(edge = 'falling')

Sets the event interrupt enable flag and configures the event interrupt for a falling (or rising) edge on the EVI pin.

When the configured edge occurs on the EVI pin the current time is copied to the "timestamp" registers and the INT pin is driven low. A call to `getEventInterrupt()` can be used to poll the interrupt status if the INT pin is not connected.

Once an event has occured a call to `getTime(eventTimestamp = True)` will return the time of the last event. 

Note that the PiicoDev Real Time Clock module has a pull-up resistor connected to the EVI pin so this function defaults to detecting a falling edge.

Parameter | Type | Default | Description
--- | --- | --- | ---
edge | String | 'falling' | If 'falling' a falling edge / low level trigger is configured on the EVI pin. If anything else a rising / high level trigger is configured.

### getEventInterrupt()

Returns the state (True or False) of the event interrupt flag. This function can be used to poll the interrupt status if the INT pin is not connected.

### setTime(time)

Sets the current time registers in the RV3028 to the time given in the `time` argument.

The `time` argument can be either a list or dictionary with the following formats:

```
time[0] = hours
time[1] = minutes
time[2] = seconds
# AM/PM indicator optional
time[3] = 'AM' # or 'PM'

time['hour'] = hours
time['min'] = minutes
time['sec'] = seconds
# AM/PM indicator optional
time['ampm'] = 'AM' # or 'PM'
```

The AM/PM value is optional to differentiate between 12hr and 24hr time. If it exists the numerical hour value is assumed to be in 12-hour format (NB: range checking is not done on this value).

If the AM/PM value is omitted (ie: if len(time) is 3) then the time is assumed to be in 24hr format.

The presence or absence of the AM/PM value also configures the RV3028 for 12hr or 24hr time.

### getTime(timeFormat = 'list', eventTimestamp = False)

Returns either the current time (in `list` or `dict` format, see `setTime()` for details) or the time of the last event timestamp (again, in either `list` or `dict` formats).

Parameter | Type | Default | Description
--- | --- | --- | ---
timeFormat | String | 'list' | If `timeFormat = 'list'` then the returned time value will be in list format. If `timeFormat = 'dict'` a dictionary will be returned.
eventTimestamp | Boolean | False | If False the current time is returned. If True the time of the last event is returned.

### setDate(date)

Sets the day/month/year date.

The `date` argument can be either a list of dictionary with the following formats:

```
date[0] = day
date[1] = month
date[2] = year

date['day'] = day
date['month'] = month
date['year'] = year
```

### getDate(timeFormat = 'list', eventTimestamp = False)

Returns either the current date (in `list` or `dict` format, see `setDate()` for details) or the date of the last event timestamp (again, in either `list` or `dict` formats).

Parameter | Type | Default | Description
--- | --- | --- | ---
timeFormat | String | 'list' | If `timeFormat = 'list'` then the returned time value will be in list format. If `timeFormat = 'dict'` a dictionary will be returned.
eventTimestamp | Boolean | False | If False the current time is returned. If True the time of the last event is returned.

### getDateTime(timeFormat = 'list', eventTimestamp = False)

Returns the date and time in a format specified by `timeFormat`.

Parameter | Type | Default | Description
--- | --- | --- | ---
timeFormat | String | 'list' | If `timeFormat = 'list'` then the time and date values will be returned in two lists `data, time = getDateTime()`. If `timeFormat = 'dict'` a dictionary will be returned with all six values included.
eventTimestamp | Boolean | False | If False the current time and date are returned. If True the time and date of the last event is returned.

### timestamp():

Returns the current time and date as a string in the format `YYYY-MM-DD HH:MM:SS`, suitable for writing to a datalogger's CSV file.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
