from datetime import datetime, timezone


def get_current_utc_datetime():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%d %H:%M:%S %Z")
