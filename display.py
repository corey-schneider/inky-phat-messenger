#!/usr/bin/python3
# coding: utf-8
# Lots of code came from https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py

import glob
import os
import sys
import time
import json
import textwrap
import logging
from json.decoder import JSONDecodeError
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

logger = logging.getLogger('Display')
logging.basicConfig(filename = 'log.txt', format='%(asctime)s [%(name)s]: %(message)s', level=logging.DEBUG) #log.txt: time [display]: message
#logging.getLogger().addHandler(logging.StreamHandler()) #print to console


config_location = "config/config.json"

# Get the current path
PATH = os.path.dirname(__file__)
SSID = os.popen("sudo iwgetid -r").read().partition('\n')[0] # TODO probably shouldn't use sudo
coords = str(requests.get("https://ipinfo.io/loc").text).partition('\n')[0]

bottom_frame_info = True    # Displays the temperature, forecast, and date at the bottom of the screen


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

# Load our config.json file
try:
    with open(config_location) as json_data_file:
        config = json.load(json_data_file)
except IOError:
    logger.error("Configuration file does not exist in config/config.json. Pull a new one from https://github.com/corey-schneider/inky-phat-messenger/blob/main/config/config.json")
    sys.exit("Configuration file does not exist in config/config.json. Pull a new one from https://github.com/corey-schneider/inky-phat-messenger/blob/main/config/config.json")

def rewrite_ssid_and_coords():
    config["ssid"] = str(SSID)
    config["coords"] = coords
    with open(config_location, "w") as f:
        json.dump(config, f)
        print("Successfully wrote SSID and coords to config.json")

# The purpose of this is to decrease the requests to the ipinfo.io API
# because it is not necessary to send dozens or hundreds of requests
# per day - this device will rarely be moved
if config["ssid"] == "" or config["coords"] == "":
    logger.info("SSIDs or coordinates are blank. Writing new ones...")
    print("SSIDs or coordinates are blank. Writing new ones...")
    rewrite_ssid_and_coords()

# if there's no weather api key, do not crash - the user just gets no weather
if config["weather_api_key"] == "":
    logger.error("You are missing the Weather API key. Please add it in config/config.json")
    print("You are missing the Weather API key. Please add it in config/config.json")

stored_coords = config["coords"]
stored_SSID = config["ssid"]
api_key = config["weather_api_key"]

logger.info("Coordinates found in configuration file is "+stored_coords)
logger.info("SSID found in configuration file is \""+stored_SSID+"\"")
logger.info("Weather API key found in configuration file is "+api_key)


if stored_SSID != SSID: # SSIDs don't match; raspberry pi has moved - weather data must be changed
    logger.info("SSIDs don't match. Changing weather location...")
    rewrite_ssid_and_coords()

if config["message"] == "":
    print("No message stored.")
    message = "Send your first message via Discord!"
else:
    message = config["message"]

paragraph = textwrap.wrap(message, width=23) #25 and 24 cut off

current_h = 10
pad = 0
for line in paragraph:
    w_size, h_size = draw.textsize(line, font=font)
    draw.text(((w - w_size)/2, current_h), line, fill=inky_display.BLACK, font=font)
    current_h += h_size + pad

if len(paragraph) >= 4:
    logger.error("Your message is too long. Remove the sentence starting with: \""+paragraph[3]+"\"")
    sys.exit(0)


# Query OpenWeatherMap to scrape current weather data
def get_weather():
    weather = {}
    lat = stored_coords.split(",")[0]
    lon = stored_coords.split(",")[1]
    res = requests.get("http://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}&units=imperial".format(lat, lon, api_key))
    if res.status_code == 200:
        data = json.loads(res.text)
        weather["summary"] = data["daily"][0]["weather"][0]["main"]
        weather["temperature"] = data["current"]["temp"]
        weather["temp-hi"] = data["daily"][0]["temp"]["max"]
        weather["temp-lo"] = data["daily"][0]["temp"]["min"]
        weather["pressure"] = data["daily"][0]["pressure"] #i"ll keep it even though we"re not using it
        return weather
    else:
        logger.error("Error while retrieving weather - status code "+str(res.status_code))
        return weather

weather = get_weather()

# This maps the weather summary to weather icons
# https://openweathermap.org/weather-conditions - Main
icon_map = {
    "snow": ["Snow"],
    "rain": ["Rain"],
    "cloud": ["Clouds"],
    "sun": ["Clear"],
    "storm": ["Thunderstorm"],
    "wind": ["Squall"],
    "atmosphere": ["Smoke", "Haze", "Dust", "Sand", "Ash"],
    "fog": ["Fog"],
    "mist": ["Mist", "Drizzle"],
    "tornado": ["Tornado"]
}

# Placeholder variables
pressure = 0
temperature = 0
temp_hi = 0
temp_lo = 0
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
    logger.warning("Warning, no weather information found!")

    # Current forecast icon
if weather_icon is not None:
    img.paste(icons[weather_icon], (0, 89), masks[weather_icon])
    logger.debug("selected weather icon is "+str(weather_icon))

else:
    draw.text((10, 90), "?", inky_display.BLACK, font=font)

if bottom_frame_info:
    draw.line((37, 100, 250, 100), fill=inky_display.BLACK)      # Bottom line for 250x122 screens
    draw.line((0, 87, 37, 87), fill=inky_display.BLACK)         # Side line
    draw.line((37, 87, 37, 100), fill=inky_display.BLACK)       # Top line line
    #TODO : add support for 212x104 screens

    # Date
    datetime = time.strftime("%b %d") # appears as "May 29" or "Jan 1"
    # More documentation on anchors can be found https://pillow.readthedocs.io/en/stable/handbook/text-anchors.html
    # Note: anchors do not work for some reason, even on Pillow 8.2.0
    draw.text((190, 102), datetime, inky_display.BLACK, font=bottomFont)

    # Temperature (in Fahrenheit)
    #draw.text((40, 103), u"{}°F".format(int(temperature)), inky_display.BLACK, font=bottomFont, align="left")
    draw.text((40, 103), u"{}°/{}° \t[{}°F]".format(int(temp_hi), int(temp_lo), int(temperature)), inky_display.BLACK, font=bottomFont, align="left")

#print(reflowed + "\n" + message + "\n")

def show_rewritten_message(msg):
    output_str = ""
    for msg in paragraph:
        output_str = output_str+"\n"+msg
    return output_str

print(show_rewritten_message(message)+"\n\n"+message+"\n")

# Display the completed canvas on Inky pHAT
inky_display.set_image(img)
inky_display.show()
