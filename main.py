#!/usr/bin/env python3

# This is based on the examples here:
# https://github.com/pimoroni/inky
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageDraw, ImageFont

# from inky.auto import auto


def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)

# try:
#     inky_display = auto(ask_user=True, verbose=True)
# except TypeError:
#     raise TypeError("You need to update the Inky library to >= v1.1.0")

# inky_display.set_rotation(180)
# try:
#     inky_display.set_border(inky_display.RED)
# except NotImplementedError:
#     pass

# Figure out scaling for display size

scale_size = 1.0
padding = 0

# if inky_display.resolution == (400, 300):
#     scale_size = 2.20
#     padding = 15

# if inky_display.resolution == (600, 448):
#     scale_size = 2.20
#     padding = 30

# if inky_display.resolution == (250, 122):
#     scale_size = 1.30
#     padding = -5

scale_size = 1.30
padding = -5
# display_height = inky_display.height
display_width = 250
display_height = 122
# display_width = inky_display.width
black_color = 0
white_color = 1
yellow_color = 2

palette = [
    0, 0, 0,        # Index 0: Black
    255, 255, 255,  # Index 1: White
    255, 191, 0,  # Index 2: Yellow
]
palette.extend([0] * (768 - len(palette)))

# Create a new canvas to draw on

img = Image.new("P", (display_width, display_height))
img.putpalette(palette)
draw = ImageDraw.Draw(img)

# Load the fonts

intuitive_font = ImageFont.truetype(Intuitive, int(22 * scale_size))
hanken_bold_font = ImageFont.truetype(HankenGroteskBold, int(35 * scale_size))
hanken_medium_font = ImageFont.truetype(HankenGroteskMedium, int(16 * scale_size))

# Grab the name to be displayed

name = "Chopmo 2"

# Top and bottom y-coordinates for the white strip

y_top = int(display_height * (5.0 / 10.0))
y_bottom = y_top + int(display_height * (4.0 / 10.0))

# Draw the red, white, and red strips

for y in range(0, y_top):
    for x in range(0, display_width):
        img.putpixel((x, y), black_color)

for y in range(y_top, y_bottom):
    for x in range(0, display_width):
        img.putpixel((x, y), white_color)

for y in range(y_bottom, display_height):
    for x in range(0, display_width):
        img.putpixel((x, y), black_color)

# Calculate the positioning and draw the "Hello" text
hello_text = "Hello"
hello_w, hello_h = getsize(hanken_bold_font, hello_text)
hello_x = int((display_width - hello_w) / 2)
hello_y = 0 + padding
draw.text((hello_x, hello_y), hello_text, white_color, font=hanken_bold_font)

# Calculate the positioning and draw the "my name is" text
mynameis_text = "my name is"
mynameis_w, mynameis_h = getsize(hanken_medium_font, mynameis_text)
mynameis_x = int((display_width - mynameis_w) / 2)
mynameis_y = hello_h + padding
draw.text((mynameis_x, mynameis_y), mynameis_text, white_color, font=hanken_medium_font)

# Calculate the positioning and draw the name text

name_w, name_h = getsize(intuitive_font, name)
name_x = int((display_width - name_w) / 2)
name_y = int(y_top + ((y_bottom - y_top - name_h) / 2))
draw.text((name_x, name_y), name, yellow_color, font=intuitive_font)

# Display the completed name badge

# inky_display.set_image(img)
# inky_display.show()
img.save("output/test.png")
