#!/usr/bin/env python3

# This is based on the examples here:
# https://github.com/pimoroni/inky
import argparse
from datetime import datetime, date
import os
from typing import Optional, Tuple
from font_hanken_grotesk import HankenGroteskBold, HankenGroteskMedium
from font_intuitive import Intuitive
from PIL import Image, ImageDraw, ImageFont
from price_fetcher import fetch_prices, get_upcoming_prices
from odometer import get_expected_odometer


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

    # Note: rotation is handled by rotating the image before display
    # set_rotation() is not available on newer inky versions

    try:
        display.set_border(display.RED)
    except (NotImplementedError, AttributeError):
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
    Prices that are 10% higher than average are shown in yellow.

    Args:
        draw: PIL ImageDraw object
        upcoming_prices: List of price entries
        scale_size: Font scaling factor
    """
    font = ImageFont.truetype(HankenGroteskMedium, int(18 * scale_size))

    # Calculate average price
    total_prices = [p["price"]["total"] for p in upcoming_prices]
    avg_price = sum(total_prices) / len(total_prices)
    high_threshold = avg_price * 1.1

    x_pos = 5
    y_pos = 5
    line_height = int(18 * scale_size)

    for price in upcoming_prices:
        price_time = datetime.fromisoformat(price["localDate"])
        time_str = price_time.strftime("%H:%M")
        price_val = price["price"]["total"]
        price_str = f"{price_val:.2f}"
        text = f"{time_str} {price_str}"

        # Use yellow for high prices, black for normal
        color = YELLOW_COLOR if price_val > high_threshold else BLACK_COLOR
        draw.text((x_pos, y_pos), text, color, font=font)
        y_pos += line_height


def render_odometer(draw, display_height, scale_size):
    """
    Render expected odometer reading at the bottom of the image.

    Args:
        draw: PIL ImageDraw object
        display_height: Display height in pixels (before rotation)
        scale_size: Font scaling factor
    """
    # Lease started July 18, 2025
    lease_start = date(2025, 7, 18)
    expected_km = get_expected_odometer(lease_start)

    font = ImageFont.truetype(HankenGroteskBold, int(18 * scale_size))
    text = f"{expected_km} km"

    # Position at bottom of portrait image (will be right side after rotation)
    x_pos = 5
    y_pos = display_height - int(25 * scale_size)

    draw.text((x_pos, y_pos), text, BLACK_COLOR, font=font)


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
    img = Image.new("P", (display_height, display_width), WHITE_COLOR)
    img.putpalette(palette)
    draw = ImageDraw.Draw(img)

    # Draw prices
    render_prices(draw, upcoming_prices, scale_size)

    # Draw odometer at bottom (before rotation)
    render_odometer(draw, display_width, scale_size)

    # Rotate 90 degrees clockwise to get landscape orientation
    img = img.rotate(-90, expand=True, fillcolor=WHITE_COLOR)

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
    upcoming = get_upcoming_prices(data, hours=8)

    # Create and output image
    img = create_image(upcoming, display_width, display_height, scale_size, palette)
    output_image(img, inky_display)


if __name__ == "__main__":
    main()
