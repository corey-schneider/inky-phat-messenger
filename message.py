#!/usr/bin/python3
# Lots of code came from https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py

import glob
import os
import sys
import argparse
import time
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

# Query Dark Sky (https://darksky.net/) to scrape current weather data
def get_weather():
    weather = {}
    coords = requests.get("https://ipinfo.io/loc")
    res = requests.get("https://darksky.net/forecast/{}/us12/en".format(",".join([str(c) for c in coords])))
    if res.status_code == 200:
        soup = BeautifulSoup(res.content, "lxml")
        curr = soup.find_all("span", "currently")
        weather["summary"] = curr[0].img["alt"].split()[0]
        weather["temperature"] = int(curr[0].find("span", "summary").text.split()[0][:-1])
        press = soup.find_all("div", "pressure")
        weather["pressure"] = int(press[0].find("span", "num").text)
        return weather
    else:
        return weather

# Dictionaries to store our icons and icon masks in
icons = {}
masks = {}

weather = get_weather()
# This maps the weather summary from Dark Sky
# to the appropriate weather icons
icon_map = {
    "snow": ["snow", "sleet"],
    "rain": ["rain"],
    "cloud": ["fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"],
    "sun": ["clear-day", "clear-night"],
    "storm": [],
    "wind": ["wind"]
}

# Placeholder variables
pressure = 0
temperature = 0
weather_icon = None

if weather:
    temperature = weather["temperature"]
    pressure = weather["pressure"]
    summary = weather["summary"]

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
    draw.text((40, 103), u"{}°F".format(temperature), inky_display.BLACK, font=bottomFont, align="left")

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
