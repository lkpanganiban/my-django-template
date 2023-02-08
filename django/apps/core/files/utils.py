from datetime import datetime, timezone


def get_time_now():
    return datetime.now(timezone.utc)
