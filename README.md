# PiicoDev® Real Time Clock (RTC) RV-3028 MicroPython Module

<!-- TODO update link URL with CE SKU -->
<!-- TODO update link title -->
This is the firmware repo for the [Core Electronics PiicoDev® Real Time Clock (RTC) RV-3028](https://core-electronics.com.au/catalog/product/view/sku/CE08239)

This module depends on the [PiicoDev Unified Library](https://github.com/CoreElectronics/CE-PiicoDev-Unified), include `PiicoDev_Unified.py` in the project directory on your MicroPython device.

See the [Quickstart Guide](https://piico.dev/p19)

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

### Instance Variables
Parameter | Type   | Range                  | Default | Description
--------- | ------ | ---------------------- | ------- | --------------------------------------------------
year      | int    | 0 - 99  or 2000 - 2099 |         | If a number between 0 and 99 is entered, the year is assumed to be between 2000 and 2099
month     | int    | 1 - 12                 |         | Month of the year
day       | Pin    | 1 - 31                 |         | Day of the month
hour      | Pin    | 0 - 23                 |         | Hour of the day
minute    | int    | 0 - 59                 |         | Minutes
second    | int    | 0 - 59                 |         | Seconds
ampm      | string | 'AM', 'PM' or '24'     | '24'    | Chose between AM, PM or 24 hour time

### setDateTime()

Sends the pre-set instance variables to the RTC chip

### getDateTime(eventTimestamp = False)

If eventTimestamp is False, populates the instance variables with the current time.
If eventTimestamp is True, populates the instance variables with the event time.

### setUnixTime(time)

Parameter | Type | Default | Description
--- | --- | --- | ---
time | Integer | None | The UNIX time to load into the RV3028's UNIX time registers. These registers hold a 32-bit integer which increments once per second.**

### getUnixTime()

Returns the current UNIX time in the RV3028. Note that this is not converted to "correct" UNIX time and is simply an integer equal to the number of seconds since reset (or call to `setUnixTime()`).

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

### timestamp():

Returns the current time and date as a string in the format `YYYY-MM-DD HH:MM:SS`, suitable for writing to a datalogger's CSV file.

# License
This project is open source - please review the LICENSE.md file for further licensing information.

If you have any technical questions, or concerns about licensing, please contact technical support on the [Core Electronics forums](https://forum.core-electronics.com.au/).

*\"PiicoDev\" and the PiicoDev logo are trademarks of Core Electronics Pty Ltd.*
