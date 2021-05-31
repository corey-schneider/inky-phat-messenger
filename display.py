#!/usr/bin/python3
# Lots of code came from https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py

import glob
import os
import sys
import argparse
import time
import json
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky.auto import auto

try:
    from bs4 import BeautifulSoup
except ImportError:
    exit("This script requires the bs4 module\nInstall with: sudo pip install beautifulsoup4==4.6.3")

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

# Get the current path
PATH = os.path.dirname(__file__)
SSID = os.popen("sudo iwgetid -r").read().partition('\n')[0] # print SSID with no new line

bottom_frame_info = True    # Displays the temperature, forecast, and date at the bottom of the screen

parser = argparse.ArgumentParser()
parser.add_argument('--message', '-m', type=str, required=True, help="The message to display on the screen")
args = parser.parse_args()

message = args.message

# This function will take a message as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that message with newlines to fit into the space required.

def reflow_message(msg, width, font):
    words = msg.split(" ")
    reflowed = ''
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n" + word

    reflowed = reflowed.rstrip()

    return reflowed


inky_display = auto()
inky_display.set_border(inky_display.WHITE)

w = inky_display.WIDTH
h = inky_display.HEIGHT

# Font stuff
font_size = 20
font = ImageFont.truetype(FredokaOne, font_size)
bottomFont = ImageFont.truetype(FredokaOne, 16)

# The amount of padding around the message. Note that
# a value of 30 means 15 pixels padding left and 15
# pixels padding right. And define max width/height
padding = 5
max_width = w - padding
max_height = h - padding
below_max_length = False


# Create the canvas to draw on
img = Image.new("P", (w, h))
draw = ImageDraw.Draw(img)

def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK, inky_display.RED)):
    """Create a transparency mask.
    Takes a paletized source image and converts it into a mask
    permitting all the colours supported by Inky pHAT (0, 1, 2)
    or an optional list of allowed colours.
    :param mask: Optional list of Inky pHAT colours to allow.
    """
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in mask:
                mask_image.putpixel((x, y), 255)

    return mask_image
    
# Dictionaries to store our icons and icon masks in
icons = {}
masks = {}

# Load our icon files and generate masks
for icon in glob.glob(os.path.join(PATH, "resources/icon-*.png")):
    icon_name = icon.split("icon-")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image
    masks[icon_name] = create_mask(icon_image)

i = 0
while not below_max_length:

    reflowed = reflow_message(message, max_width, font)
    p_w, p_h = font.getsize(reflowed)       # Width and height of message
    p_h = p_h * (reflowed.count("\n") + 1)  # Multiply through by number of lines

    if p_h < max_height:
        below_max_length = True             # The message fits! Break out of the loop.

    # cheap hax
    if i > 1:
        sys.exit("Your message is too long.")

    else:
        i += 1
        continue

# x- and y-coordinates for the top left of the message
message_x = (w - max_width) / 2
message_y = ((h - max_height) + (max_height - p_h - font.getsize("ABCD ")[1])) / 2     # pushes text up top
#message_y = ((h - max_height) + (max_height - p_h)) / 2     # keeps text centered


draw.multiline_text((message_x, message_y), reflowed, fill=inky_display.BLACK, font=font, align="center")

def write_coords():
    print("Coordinates not found! Writing new coordinates.")
    tempCoord = open("config/coords.txt", "w")
    tempCoord.write(str(requests.get("https://ipinfo.io/loc").text).partition('\n')[0])
    print("Coordinates successfully written.")
    tempCoord.close()

def write_ssid():
    print("SSID not saved! Writing new SSID.")
    tempSSID = open("config/ssid.txt", "w")
    tempSSID.write(str(SSID))
    print("SSID successfully written.")
    tempSSID.close()

# The purpose of this is to decrease the requests to the ipinfo.io API
# because it is not necessary to send dozens or hundreds of requests
# per day - this project will rarely be moved
if os.path.getsize("config/coords.txt") == 0:
    write_coords()

if os.path.getsize("config/ssid.txt") == 0:
    write_ssid()

if os.path.getsize("../api.txt") == 0: #TODO change this on release
    print("You are missing the Weather API key. Please add it in config/api.txt")

tempCoord = open("config/coords.txt", "r")
coords = tempCoord.readline()
tempCoord.close()

tempSSID = open("config/ssid.txt", "r")
storedSSID = tempSSID.readline()
tempSSID.close()

temp_api_key = open("../api.txt", "r")
api_key = temp_api_key.readline()
temp_api_key.close()


print("Coordinates found in config/coords.txt is "+coords)
print("SSID found in config/ssid.txt is "+storedSSID)
print("Weather API key found in config/api.txt is "+api_key)


if storedSSID != SSID: # SSIDs don't match; box has moved, weather data must be changed
    print("SSIDs don't match. Changing weather location...")

    open("config/coords.txt", "w").close() #erase saved coords
    write_coords()

    open("config/ssid.txt", "w").close() #erase saved ssid
    write_ssid()

# Query OpenWeatherMap to scrape current weather data
def get_weather():
    weather = {}
    lat = coords.split(",")[0]
    lon = coords.split(",")[1]
    res = requests.get("http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=imperial".format(lat, lon, api_key))
    if res.status_code == 200:
        data = json.loads(res.text)
        weather["summary"] = data["weather"][0]["main"]
        weather["temperature"] = data["main"]["temp"] #current temp
        weather["temp-hi"] = data["main"]["temp_max"]
        weather["temp-lo"] = data["main"]["temp_min"]
        weather["pressure"] = data["main"]["pressure"] #i"ll keep it even though we"re not using it
        return weather
    else:
        return weather

weather = get_weather()

# This maps the weather summary to weather icons
# https://openweathermap.org/weather-conditions - Main
icon_map = {
    "snow": ["Snow"],
    "rain": ["Drizzle", "Rain"],
    "cloud": ["Clouds"],
    "sun": ["Clear"],
    "storm": ["Thunderstorm", "Tornado"],
    "wind": ["Squall"],
    "atmosphere": ["Mist", "Smoke", "Haze", "Dust", "Fog", "Sand", "Ash", "Tornado"]
}

# Placeholder variables
pressure = 0
temperature = 0
weather_icon = None

if weather:
    summary = weather["summary"]
    temperature = weather["temperature"]
    temp_hi = weather["temp-hi"]
    temp_lo = weather["temp-lo"]
    pressure = weather["pressure"]

    for icon in icon_map:
        if summary in icon_map[icon]:
            weather_icon = icon
            break

else:
    print("Warning, no weather information found!")

if bottom_frame_info:
    draw.line((37, 100, 250, 100), fill=inky_display.BLACK)      # Bottom line for 250x122 screens
    draw.line((0, 87, 37, 87), fill=inky_display.BLACK)         # Side line
    draw.line((37, 87, 37, 100), fill=inky_display.BLACK)       # Top line line
    #TODO : add support for 212x104 screens

    # Date
    datetime = time.strftime("%b %d") # appears as "May 29" or "Jan 1"
    draw.text((180, 102), datetime, inky_display.BLACK, font=bottomFont, align="right")

    # Temperature (in Fahrenheit)
    draw.text((40, 103), u"{}°F".format(int(temperature)), inky_display.BLACK, font=bottomFont, align="left")

    # Current forecast icon (updated whenever the script is run - do a cron job hourly)
if weather_icon is not None:
    img.paste(icons[weather_icon], (0, 89), masks[weather_icon])
    print("selected icon is "+str(weather_icon))

else:
    draw.text((10, 90), "?", inky_display.BLACK, font=font)

print(reflowed + "\n" + message + "\n")

# Display the completed canvas on Inky pHAT
inky_display.set_image(img)
inky_display.show()
