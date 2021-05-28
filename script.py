#!/usr/bin/python3
# Copyright 2020 Harlen Bains
# linted using pylint
# formatted using black
"""This script takes in one agrgument and then displays it on a InkyPhat
display"""
import sys
from PIL import Image, ImageFont, ImageDraw  # pylint: disable=import-error
from font_fredoka_one import FredokaOne  # pylint: disable=import-error
from inky.auto import auto  # pylint: disable=import-error


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


print_text(str(sys.argv[1]))