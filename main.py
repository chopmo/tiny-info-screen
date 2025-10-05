#!/usr/bin/env python3

# This is based on the examples here:
# https://github.com/pimoroni/inky
import argparse
from datetime import datetime
import os
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageDraw, ImageFont
from price_fetcher import fetch_prices, get_upcoming_prices


def getsize(font, text):
    _, _, right, bottom = font.getbbox(text)
    return (right, bottom)


# Parse command line arguments
parser = argparse.ArgumentParser(description='Display electricity prices on InkyPHAT or save to PNG')
parser.add_argument('--dev', action='store_true', help='Development mode: save to PNG instead of displaying on InkyPHAT')
args = parser.parse_args()

# Set development mode environment variable
if args.dev:
    os.environ["DEV_MODE"] = "1"

# Check if we're in development mode
dev_mode = os.getenv("DEV_MODE")

# Initialize display if in production mode
inky_display = None
if not dev_mode:
    from inky.auto import auto
    try:
        inky_display = auto(ask_user=True, verbose=True)
    except TypeError:
        raise TypeError("You need to update the Inky library to >= v1.1.0")

    inky_display.set_rotation(180)
    try:
        inky_display.set_border(inky_display.RED)
    except NotImplementedError:
        pass

# Figure out scaling for display size
scale_size = 1.0
padding = 0

if inky_display:
    if inky_display.resolution == (400, 300):
        scale_size = 2.20
        padding = 15
    elif inky_display.resolution == (600, 448):
        scale_size = 2.20
        padding = 30
    elif inky_display.resolution == (250, 122):
        scale_size = 1.30
        padding = -5

    display_width = inky_display.width
    display_height = inky_display.height
else:
    # Development mode defaults
    scale_size = 1.30
    padding = -5
    display_width = 250
    display_height = 122
black_color = 0
white_color = 1
yellow_color = 2

palette = [
    0, 0, 0,        # Index 0: Black
    255, 255, 255,  # Index 1: White
    255, 191, 0,  # Index 2: Yellow
]
palette.extend([0] * (768 - len(palette)))

# Fetch electricity prices
data = fetch_prices()
upcoming = get_upcoming_prices(data, hours=5)

# Create a new canvas to draw on
img = Image.new("P", (display_width, display_height))
img.putpalette(palette)
draw = ImageDraw.Draw(img)

# Load the fonts
small_font = ImageFont.truetype(HankenGroteskMedium, int(12 * scale_size))
medium_font = ImageFont.truetype(HankenGroteskMedium, int(14 * scale_size))

# Fill background with white
for y in range(0, display_height):
    for x in range(0, display_width):
        img.putpixel((x, y), white_color)

# Draw prices
y_pos = 5
for i, price in enumerate(upcoming):
    # Parse time from localDate (format: "2025-10-04T00:00:00")
    price_time = datetime.fromisoformat(price["localDate"])
    time_str = price_time.strftime("%H:%M")

    # Format price with 2 decimal places
    price_val = price["price"]["total"]
    price_str = f"{price_val:.2f} kr"

    # Draw time and price on the same line
    text = f"{time_str}  {price_str}"
    draw.text((10, y_pos), text, black_color, font=medium_font)

    y_pos += int(20 * scale_size)

# Display the completed name badge
if inky_display:
    inky_display.set_image(img)
    inky_display.show()
else:
    img.save("output/test.png")
    print("Development mode: Image saved to output/test.png")
