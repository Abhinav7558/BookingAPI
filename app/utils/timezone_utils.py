import os
import pytz
from datetime import datetime, timezone


def get_default_timezone() -> str:
    """Get the default timezone from environment or return IST"""
    return os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")

def convert_timezone_to_utc(local_datetime: datetime, source_timezone: str = None) -> datetime:
    """
    Convert local datetime to UTC
    """
    if source_timezone is None:
        source_timezone = get_default_timezone()
    
    # If datetime is naive, localize it to source timezone
    if local_datetime.tzinfo is None:
        source_tz = pytz.timezone(source_timezone)
        local_datetime = source_tz.localize(local_datetime)
    
    # Convert to UTC
    return local_datetime.astimezone(timezone.utc)