import os
import pytz
from datetime import datetime, timezone


def get_default_timezone() -> str:
    """Get the default timezone from environment or return IST"""
    return os.getenv("DEFAULT_TIMEZONE", "Asia/Kolkata")

def convert_utc_to_timezone(utc_datetime: datetime, target_timezone: str = None) -> datetime:
    """
    Convert UTC datetime to specified timezone
    """
    if target_timezone is None:
        target_timezone = get_default_timezone()
    
    # Ensure the datetime is timezone-aware (UTC)
    if utc_datetime.tzinfo is None:
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)
    elif utc_datetime.tzinfo != timezone.utc:
        utc_datetime = utc_datetime.astimezone(timezone.utc)
    
    # Convert to target timezone
    target_tz = pytz.timezone(target_timezone)
    return utc_datetime.astimezone(target_tz)

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

def is_valid_timezone(timezone_str: str) -> bool:
    """
    Check if timezone string is valid
    """
    try:
        pytz.timezone(timezone_str)
        return True
    except pytz.UnknownTimeZoneError:
        return False