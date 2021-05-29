#!/usr/bin/python3
# Lots of code came from https://github.com/pimoroni/inky/blob/master/examples/what/quotes-what.py

import sys
import argparse
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky.auto import auto

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

if bottom_frame_info:
    draw.line((0, 82, 212, 82))      # Bottom line

print(reflowed + "\n" + message + "\n")

# Display the completed canvas on Inky pHAT
inky_display.set_image(img)
inky_display.show()
