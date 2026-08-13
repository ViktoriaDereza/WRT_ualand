from datetime import datetime, timedelta, timezone

class DataGenerator:
    @staticmethod
    def current_date():
        return datetime.now().strftime("%d.%m.%Y")


    def current_time_plus_any_minutes(minutes: int):
        future_time = datetime.now() + timedelta(minutes=minutes)
        return future_time.strftime("%H:%M")

    @staticmethod
    def utc_time_plus_minutes_iso(minutes: int):
        future_time = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        return future_time.isoformat(timespec="milliseconds").replace("+00:00", "Z")

