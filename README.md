# Weather + Clock OLED display for Raspberry Pi 3
This is a little demo using a SPI 0.96" oled display (it should support I2C too without problems).
![Demo image of oled screen](https://i.imgur.com/ZS4vXCP.gif)

This is the one I used: https://www.adafruit.com/product/326

It uses the [Adafruit_Python_SSD1306 Library](https://github.com/adafruit/Adafruit_Python_SSD1306), designed for [these displays](https://www.adafruit.com/categories/98).

- Make sure you get an API key for the weather: [https://darksky.net/dev/docs](https://darksky.net/dev/docs)
- Make sure you read the Raspberry PI 3 SPI pinout: [https://pinout.xyz/pinout/spi](https://pinout.xyz/pinout/spi) (or I2C if you used that). I used the SPI0 port, GPIO 25 for RESET and GPIO 24 for DC.

Depending on what oled board you use, your pins might have different names. Took me a while to get mine to work. Maybe these little charts will help you:

|OLED Pin | Name | Remarks      | RPi Pin | RPi Function    |
|---------|:----:|-------------:|--------:|----------------:|
| 1       | VCC  | +3.3V Power  | P01-17  | 3V3             |
| 2       | GND  | Ground       | P01-20  | GND             |
| 3       | D0   | Clock        | P01-23  | GPIO 11 (SCLK)  |
| 4       | D1   | MOSI         | P01-19  | GPIO 10 (MOSI)  |
| 5       | RST  | Reset        | P01-22  | GPIO 25         |
| 6       | DC   | Data/Command | P01-18  | GPIO 24         |
| 7       | CS   | Chip Select  | P01-24  | GPIO 8 (CE0)    |

| Pin  | Alternate Names |Description  |
|------|:---------------:|------------:|
| VCC  |                 |Power supply |
| GND  |                 |Ground       |
| D0   | SCL,CLK,SCK     |Clock        |
| D1   | SDA,MOSI        |Data         |
| RES  | RST,RESET       |Rest         |
| DC   | A0              |Data/Command |
| CS   |                 |Chip Select  |

Icons made by [iconixar](https://www.flaticon.com/packs/weather-200) from [www.flaticon.com](https://www.flaticon.com/) licensed by [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/)

