# -*- coding: utf-8 -*-
import time
import datetime
import requests
import psutil
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Raspberry Pi pin configuration:
RST = 25     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware SPI:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0
x_scroll = 0

# Tiempo por pantalla
segundos_x_pantalla = 3

# CLIMA (GET YOUR API KEY: https://darksky.net/dev/docs)
f_api_key   = open("api_key.txt", "r")
api_key     = f_api_key.read()
f_api_key.close()
location    = "-26.830139,-65.225670"
fetchUrl    = "https://api.darksky.net/forecast/"+api_key+"/"+location+"?units=si&lang=es"
result      = False
timer_start = time.time()
timer_end   = time.time()

# FUNCION PARA LIMPIAR DISPLAY
def clear_image():
    global draw, width, height
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

# FUNCION PARA MOSTRAR PANTALLA
def show_image(img=image):
    disp.image(img)
    disp.display()

# FUNCION PARA MOSTRAR RELOJ
def display_clock():
    global segundos_x_pantalla
    fontsize = 50
    font     = ImageFont.truetype('./UbuntuMono-Bold.ttf', fontsize)

    # Show date
    clear_image()
    now = datetime.datetime.now()
    draw.text((x + 2, top + 5), now.strftime("%d/%m"),  font=font, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Show time
    clear_image()
    draw.text((x + 2, top + 5), now.strftime("%H:%M"),  font=font, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

# FUNCIONES PARA MOSTRAR CLIMA
def update_clima():
    global result, timer_start, timer_end
    timer_end = time.time()
    # Get weather every 10 minutes
    if ((timer_end - timer_start) > 10*60) or not result:
        # print("requesting weather...\n")
        r=requests.get(fetchUrl)
        result = r.json()
        timer_start = time.time()

def display_clima():
    global result, segundos_x_pantalla
    fontsize = 75
    fontsizes2 = 45
    fontsizes = 30
    fontsizexs = 14
    font     = ImageFont.truetype('./UbuntuMono-Bold.ttf', fontsize)
    fonts    = ImageFont.truetype('./UbuntuMono-Bold.ttf', fontsizes)
    fonts2   = ImageFont.truetype('./UbuntuMono-Bold.ttf', fontsizes2)
    fontxs   = ImageFont.truetype('./UbuntuMono-Bold.ttf', fontsizexs)

    # Show today icon
    clear_image()
    icon = Image.open('icons/' + result["currently"]["icon"] + '.ppm').convert('1')
    drawIcon = ImageDraw.Draw(icon)
    drawIcon.text((x, top), result["currently"]["summary"] ,  font=fontxs, fill=255)
    show_image(icon)
    time.sleep(segundos_x_pantalla)

    # Current temperature
    clear_image()
    draw.text((x + 5, top - 3), str(int(result["currently"]["temperature"])),  font=font, fill=255)
    draw.text((x + 90, top + 8), u"°C",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Current apparent temperature
    clear_image()
    draw.text((x + 5, top - 3), str(int(result["currently"]["apparentTemperature"])),  font=font, fill=255)
    draw.text((x + 90, top + 8), u"°C",  font=fonts, fill=255)
    draw.text((x + 90, top + 35), "st",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Tomorrow icon
    clear_image()
    icon = Image.open('icons/' + result["daily"]["data"][1]["icon"] + '.ppm').convert('1')
    drawIcon = ImageDraw.Draw(icon)
    drawIcon.text((x, top), u'Mañana:',  font=fontxs, fill=255)
    show_image(icon)
    time.sleep(segundos_x_pantalla)

    # Tomorrow HIGH temperature
    clear_image()
    draw.text((x, top), u'Mañana máxima:',  font=fontxs, fill=255)
    draw.text((x + 5, top + 2), str(int(result["daily"]["data"][1]["temperatureHigh"])),  font=font, fill=255)
    draw.text((x + 90, top + 10), u"°C",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Tomorrow apparent HIGH temperature
    clear_image()
    draw.text((x, top), u'Mañana máxima:',  font=fontxs, fill=255)
    draw.text((x + 5, top + 2), str(int(result["daily"]["data"][1]["apparentTemperatureHigh"])),  font=font, fill=255)
    draw.text((x + 90, top + 10), u"°C",  font=fonts, fill=255)
    draw.text((x + 90, top + 37), "st",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Tomorrow Low temperature
    clear_image()
    draw.text((x, top), u'Mañana mínima:',  font=fontxs, fill=255)
    draw.text((x + 5, top + 2), str(int(result["daily"]["data"][1]["temperatureLow"])),  font=font, fill=255)
    draw.text((x + 90, top + 10), u"°C",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Tomorrow apparent Low temperature
    clear_image()
    draw.text((x, top), u'Mañana mínima:',  font=fontxs, fill=255)
    draw.text((x + 5, top + 2), str(int(result["daily"]["data"][1]["apparentTemperatureLow"])),  font=font, fill=255)
    draw.text((x + 90, top + 10), u"°C",  font=fonts, fill=255)
    draw.text((x + 90, top + 37), "st",  font=fonts, fill=255)
    show_image()
    time.sleep(segundos_x_pantalla)

    # Week summary
    scroll = 0
    (font_size_x, font_size_y) = fonts2.getsize(result["daily"]["summary"])
    (char_width, _) = fonts2.getsize("a");
    while -1*scroll <= (font_size_x + char_width + width):
        clear_image()
        draw.text((x, top), u'Resumen semanal:',  font=fontxs, fill=255)
        draw.text((x + width + scroll, top + 18), result["daily"]["summary"],  font=fonts2, fill=255)
        show_image()
        scroll -= char_width
        time.sleep(.25)

while True:
    display_clock()
    update_clima()
    display_clima()