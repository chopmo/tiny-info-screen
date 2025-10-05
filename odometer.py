"""Calculate expected odometer reading for leased car."""

from datetime import datetime, date


def get_expected_odometer(
    lease_start_date: date,
    total_km_allowed: int = 20000,
    lease_duration_days: int = 365
) -> int:
    """
    Calculate expected odometer reading based on lease terms.

    Args:
        lease_start_date: Date when the lease started
        total_km_allowed: Total kilometers allowed during lease
        lease_duration_days: Duration of lease in days

    Returns:
        Expected odometer reading as integer
    """
    today = date.today()
    days_elapsed = (today - lease_start_date).days

    # Calculate expected km based on daily allowance
    daily_allowance = total_km_allowed / lease_duration_days
    expected_km = int(days_elapsed * daily_allowance)

    return expected_km


if __name__ == "__main__":
    # Example: Lease started July 18, 2025
    lease_start = date(2025, 7, 18)
    expected = get_expected_odometer(lease_start)
    print(f"Expected odometer: {expected} km")
