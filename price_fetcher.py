"""Fetch and parse electricity prices from Strømligning.dk API."""

import requests
from typing import Dict, List, Any


def fetch_prices(price_area: str = "DK1") -> Dict[str, Any]:
    """
    Fetch latest electricity prices from Strømligning.dk API.

    Args:
        price_area: Price area code (default: "DK1")

    Returns:
        Parsed JSON response containing price data

    Raises:
        requests.RequestException: If the API request fails
    """
    # Based on API docs at https://stromligning.dk/api/docs/
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
