from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from ..utils.timezone_utils import convert_utc_to_timezone, convert_timezone_to_utc, is_valid_timezone

def test_convert_utc_to_timezone():
    now_utc = datetime(2025, 6, 10, 12, 0, tzinfo=timezone.utc)
    converted = convert_utc_to_timezone(now_utc, "Asia/Kolkata")
    assert converted.tzinfo is not None
    assert converted.isoformat().endswith("+05:30")

def test_convert_timezone_to_utc():
    now_utc = datetime(2025, 6, 10, 12, 0, tzinfo=ZoneInfo("Asia/kolkata"))
    converted = convert_utc_to_timezone(now_utc, "UTC")
    assert converted.tzinfo is not None
    assert converted.isoformat().endswith("+00:00")

def test_invalid_timezone_check():
    assert is_valid_timezone("Asia/Kolkata")
    assert not is_valid_timezone("Invalid/Zone")
