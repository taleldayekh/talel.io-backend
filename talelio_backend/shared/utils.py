from datetime import datetime, timedelta


def generate_time_from_now(seconds: int) -> datetime:
    return datetime.utcnow() + timedelta(seconds=seconds)
