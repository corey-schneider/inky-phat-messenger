#!/usr/bin/python3

import sys
import argparse
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky.auto import auto


# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.

def reflow_quote(quote, width, font):
    words = quote.split(" ")
    reflowed = '"'
    line_length = 0

    for i in range(len(words)):
        word = words[i] + " "
        word_length = font.getsize(word)[0]
        line_length += word_length

        if line_length < width:
            reflowed += word
        else:
            line_length = word_length
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip() + '"'

    return reflowed


inky_display = auto()
inky_display.set_border(inky_display.WHITE)

w = inky_display.WIDTH
h = inky_display.HEIGHT

# Font stuff
font_size = 20
font = ImageFont.truetype(FredokaOne, font_size)

# The amount of padding around the quote. Note that
# a value of 30 means 15 pixels padding left and 15
# pixels padding right. And define max width/height
padding = 30
max_width = w - padding
max_height = h - padding - font.getsize("ABCD ")[1]
below_max_length = False


def print_text(text):
    """Displays text in Inky pHAT display.
    Args:
        text: String that is displayed on the Inky pHAT
    """
    img = Image.new("P", (w, h))
    draw = ImageDraw.Draw(img)
    
    message = text
    width, height = font.getsize(message)
    x_axis = (w / 2) - (width / 2)
    y_axis = (h / 2) - (height / 2)
    draw.text((x_axis, y_axis), message, inky_display.BLACK, font)
    inky_display.set_image(img)
    inky_display.show()

parser = argparse.ArgumentParser()
parser.add_argument('--message', '-m', type=str, required=True, help="The message to display on the screen")
args = parser.parse_args()

message = args.message

print_text(message)