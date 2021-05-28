#!/usr/bin/python3

import sys
import argparse
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky.auto import auto


parser = argparse.ArgumentParser()
parser.add_argument('--message', '-m', type=str, required=True, help="The message to display on the screen")
args = parser.parse_args()

message = args.message

# This function will take a quote as a string, a width to fit
# it into, and a font (one that's been loaded) and then reflow
# that quote with newlines to fit into the space required.

def reflow_quote(quote, width, font):
    words = quote.split(" ")
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
            reflowed = reflowed[:-1] + "\n  " + word

    reflowed = reflowed.rstrip()

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


# Create the canvas to draw on
img = Image.new("P", (w, h))
draw = ImageDraw.Draw(img)


while not below_max_length:

    reflowed = reflow_quote(message, max_width, font)
    p_w, p_h = font.getsize(reflowed)  # Width and height of quote
    p_h = p_h * (reflowed.count("\n") + 1)   # Multiply through by number of lines

    if p_h < max_height:
        below_max_length = True              # The quote fits! Break out of the loop.

    else:
        continue

# x- and y-coordinates for the top left of the quote
message_x = (w - max_width) / 2
message_y = ((h - max_height) + (max_height - p_h - font.getsize("ABCD ")[1])) / 2


draw.multiline_text((message_x, message_y), reflowed, fill=inky_display.BLACK, font=font, align="left")

print(reflowed + "\n" + message + "\n")

# Display the completed canvas on Inky wHAT
inky_display.set_image(img)
inky_display.show()

# def print_text(message):
#     width, height = font.getsize(message)
#     x_axis = (w / 2) - (width / 2)
#     y_axis = (h / 2) - (height / 2)
#     draw.text((x_axis, y_axis), message, inky_display.BLACK, font)
#     inky_display.set_image(img)
#     inky_display.show()


# print_text(message)