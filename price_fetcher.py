"""Fetch and parse electricity prices from Strømligning.dk API."""

import json
import os
from pathlib import Path
import requests
from typing import Dict, List, Any


def fetch_prices(price_area: str = "DK1") -> Dict[str, Any]:
    """
    Fetch latest electricity prices from Strømligning.dk API.

    In development mode (when DEV_MODE env var is set), reads from
    example-response.json instead of making API requests.

    Args:
        price_area: Price area code (default: "DK1")

    Returns:
        Parsed JSON response containing price data

    Raises:
        requests.RequestException: If the API request fails
        FileNotFoundError: If example-response.json doesn't exist in dev mode
    """
    # Check for development mode
    if os.getenv("DEV_MODE"):
        cache_file = Path(__file__).parent / "example-response.json"
        if not cache_file.exists():
            raise FileNotFoundError(
                f"Development mode enabled but {cache_file} not found. "
                "Run ./bin/fetch-prices to create it."
            )
        with open(cache_file, 'r') as f:
            return json.load(f)

    # Production mode: fetch from API
    url = "https://stromligning.dk/api/prices"
    params = {
        "priceArea": price_area,
        "aggregation": "1h"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def get_hourly_prices(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract hourly price data from API response.

    Args:
        data: Parsed JSON response from fetch_prices()

    Returns:
        List of hourly price entries with date and price information
    """
    return data.get("prices", [])


if __name__ == "__main__":
    # Example usage
    try:
        data = fetch_prices()
        prices = get_hourly_prices(data)
        print(f"Fetched {len(prices)} hourly prices")
        print("\nNext 4 hours:")
        for price in prices[:4]:
            print(f"{price['localDate']} - {price['price']['total']:.3f} {price['price']['unit']}")
    except Exception as e:
        print(f"Error fetching prices: {e}")
