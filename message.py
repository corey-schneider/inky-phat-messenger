#!/usr/bin/python3

import sys
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky.auto import auto


def print_text(text):
    """Displays text in Inky pHAT display.
    Args:
        text: String that is displayed on the Inky pHAT
    """
    inky_display = auto()
    inky_display.set_border(inky_display.WHITE)
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FredokaOne, 18)
    message = text
    width, height = font.getsize(message)
    x_axis = (inky_display.WIDTH / 2) - (width / 2)
    y_axis = (inky_display.HEIGHT / 2) - (height / 2)
    draw.text((x_axis, y_axis), message, inky_display.BLACK, font)
    inky_display.set_image(img)
    inky_display.show()

parser = argparse.ArgumentParser()
parser.add_argument('--message', '-m', type=str, required=True, help="The message to display on the screen")
args = parser.parse_args()

message = args.message

print_text(message)