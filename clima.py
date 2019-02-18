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
segundos_x_pantalla = 10

# CLIMA (GET YOUR API KEY: https://darksky.net/dev/docs)
f_api_key   = open("api_key.txt", "r")
api_key     = f_api_key.read()
f_api_key.close()
location    = "-26.830139,-65.225670"
fetchUrl    = "https://api.darksky.net/forecast/"+api_key+"/"+location+"?units=si"
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
    count    = 0
    fontsize = 42
    font     = ImageFont.truetype('ptmono.ttf', fontsize)

    while count <= segundos_x_pantalla:
        clear_image()
        now = datetime.datetime.now()
        draw.text((x, top + 10), now.strftime("%d/%m"),  font=font, fill=255)
        show_image()
        time.sleep(2)

        clear_image()
        draw.text((x, top + 10), now.strftime("%H:%M"),  font=font, fill=255)
        show_image()
        time.sleep(2)

        # Incremento 4 porque mostre 2 cosas por 2 segundos
        count += 4

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
    global result
    count    = 0
    fontsize = 60
    fontsizes = 30
    font     = ImageFont.truetype('ptmono.ttf', fontsize)
    fonts     = ImageFont.truetype('ptmono.ttf', fontsizes)

    icon = Image.open('icons/' + result["currently"]["icon"] + '.ppm').convert('1')

    while count <= segundos_x_pantalla:
        clear_image()
        show_image(icon)
        time.sleep(2)

        clear_image()
        draw.text((x + 2, top + 5), str(int(result["currently"]["temperature"])),  font=font, fill=255)
        draw.text((x + 90, top + 8), "C",  font=fonts, fill=255)
        show_image()
        time.sleep(2)

        clear_image()
        draw.text((x + 2, top + 5), str(int(result["currently"]["apparentTemperature"])),  font=font, fill=255)
        draw.text((x + 90, top + 8), "C",  font=fonts, fill=255)
        draw.text((x + 90, top + 35), "st",  font=fonts, fill=255)
        show_image()
        time.sleep(2)

        count += 5

while True:
    display_clock()
    update_clima()
    display_clima()