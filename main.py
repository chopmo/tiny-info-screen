#!/usr/bin/env python3

# This is based on the examples here:
# https://github.com/pimoroni/inky
import argparse
from datetime import datetime
import os
from typing import Optional, Tuple
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageDraw, ImageFont
from price_fetcher import fetch_prices, get_upcoming_prices


# Color constants
BLACK_COLOR = 0
WHITE_COLOR = 1
YELLOW_COLOR = 2


def init_display():
    """Initialize InkyPHAT display in production mode."""
    from inky.auto import auto
    try:
        display = auto(ask_user=True, verbose=True)
    except TypeError:
        raise TypeError("You need to update the Inky library to >= v1.1.0")

    display.set_rotation(180)
    try:
        display.set_border(display.RED)
    except NotImplementedError:
        pass

    return display


def get_display_config(inky_display) -> Tuple[int, int, float, int]:
    """
    Get display configuration based on display type.

    Returns:
        Tuple of (width, height, scale_size, padding)
    """
    if inky_display:
        width = inky_display.width
        height = inky_display.height

        if inky_display.resolution == (400, 300):
            scale_size = 2.20
            padding = 15
        elif inky_display.resolution == (600, 448):
            scale_size = 2.20
            padding = 30
        elif inky_display.resolution == (250, 122):
            scale_size = 1.30
            padding = -5
        else:
            scale_size = 1.0
            padding = 0
    else:
        # Development mode defaults
        width = 250
        height = 122
        scale_size = 1.30
        padding = -5

    return width, height, scale_size, padding


def create_palette():
    """Create color palette for the display."""
    palette = [
        0, 0, 0,        # Index 0: Black
        255, 255, 255,  # Index 1: White
        255, 191, 0,    # Index 2: Yellow
    ]
    palette.extend([0] * (768 - len(palette)))
    return palette


def render_prices(draw, upcoming_prices, scale_size):
    """
    Render electricity prices on the image.

    Args:
        draw: PIL ImageDraw object
        upcoming_prices: List of price entries
        scale_size: Font scaling factor
    """
    medium_font = ImageFont.truetype(HankenGroteskMedium, int(14 * scale_size))

    y_pos = 5
    for price in upcoming_prices:
        # Parse time from localDate (format: "2025-10-04T00:00:00")
        price_time = datetime.fromisoformat(price["localDate"])
        time_str = price_time.strftime("%H:%M")

        # Format price with 2 decimal places
        price_val = price["price"]["total"]
        price_str = f"{price_val:.2f}"

        # Draw time and price on the same line
        text = f"{time_str}  {price_str}"
        draw.text((10, y_pos), text, BLACK_COLOR, font=medium_font)

        y_pos += int(20 * scale_size)


def create_image(upcoming_prices, display_width, display_height, scale_size, palette):
    """
    Create the image to display.

    Args:
        upcoming_prices: List of price entries
        display_width: Display width in pixels
        display_height: Display height in pixels
        scale_size: Font scaling factor
        palette: Color palette

    Returns:
        PIL Image object
    """
    # Create image in portrait orientation (will be rotated 90 degrees)
    img = Image.new("P", (display_height, display_width))
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    # Fill background with white
    for y in range(0, display_width):
        for x in range(0, display_height):
            img.putpixel((x, y), WHITE_COLOR)

    # Draw prices
    render_prices(draw, upcoming_prices, scale_size)

    # Rotate 90 degrees clockwise to get landscape orientation
    img = img.rotate(-90, expand=True)

    return img


def output_image(img, inky_display):
    """
    Output image to display or save to file.

    Args:
        img: PIL Image object
        inky_display: InkyPHAT display object or None
    """
    if inky_display:
        inky_display.set_image(img)
        inky_display.show()
    else:
        img.save("output/test.png")
        print("Development mode: Image saved to output/test.png")


def main():
    """Main function."""
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
        inky_display = init_display()

    # Get display configuration
    display_width, display_height, scale_size, padding = get_display_config(inky_display)

    # Create color palette
    palette = create_palette()

    # Fetch electricity prices
    data = fetch_prices()
    upcoming = get_upcoming_prices(data, hours=5)

    # Create and output image
    img = create_image(upcoming, display_width, display_height, scale_size, palette)
    output_image(img, inky_display)


if __name__ == "__main__":
    main()
