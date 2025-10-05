# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Display local electricity prices for the coming hours on a small e-paper display (InkyPHAT). The goal is to make it easy to see when it's least expensive to charge cars.

## Development Commands

**Install dependencies:**
```bash
pip3 install -r requirements.txt
```

**Run the script:**
```bash
python3 main.py
```

**Watch mode (auto-reload on file changes):**
```bash
while inotifywait -e close_write main.py; do python3 ./main.py; done
```

## Architecture

### Current State
- The InkyPHAT display code is currently commented out in main.py
- Script outputs to `output/test.png` instead of the physical display
- This is useful for development without hardware

### Display Specifications
- Resolution: 250x122 pixels
- 3-color palette: black (0), white (1), yellow (2)
- Based on Pimoroni Inky library examples

### Data Source
- Expects Danish electricity price data (DK1 price area)
- API response structure documented in `example-response.json`
- Format: hourly prices with total, VAT, electricity cost, and transmission tariffs
- Currency: kr/kWh

### Rendering
- Uses PIL (Pillow) for image generation
- Fonts: Hanken Grotesk (Bold/Medium) and Intuitive
- Scale factor and padding adjusted for 250x122 display
