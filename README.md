# Weather + Clock OLED display for Raspberry Pi 3
This is a little demo using a SPI 0.96" oled display (it should support I2C too without problems). 
![Demo image of oled screen](https://i.imgur.com/ZS4vXCP.gif)

This is the one I used: https://www.adafruit.com/product/326

It uses the [Adafruit_Python_SSD1306 Library](https://github.com/adafruit/Adafruit_Python_SSD1306), designed for [these displays](https://www.adafruit.com/categories/98).

- Make sure you get an API key for the weather: [https://darksky.net/dev/docs](https://darksky.net/dev/docs)
- Make sure you read the Raspberry PI 3 SPI pinout: [https://pinout.xyz/pinout/spi](https://pinout.xyz/pinout/spi) (or I2C if you used that). I used the SPI0 port, GPIO 25 for RESET and GPIO 24 for DC.

Depending on what oled board you use, your pins might have different names. Took me a while to get mine to work. Maybe this little chart will help you with different names:

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

