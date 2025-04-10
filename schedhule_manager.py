from schedhule import *
from datetime import datetime
from zoneinfo import ZoneInfo

class ScheduleContextGenerator:
  SCHEDULES = {
        0: MONDAY_SCHEDULE,  # Monday
        1: TUESDAY_SCHEDULE,  # Tuesday
        2: WEDNESDAY_SCHEDULE,  # Wednesday
        3: THURSDAY_SCHEDULE,  # Thursday
        4: FRIDAY_SCHEDULE,  # Friday
        5: SATURDAY_SCHEDULE,  # Saturday
        6: SUNDAY_SCHEDULE,  # Sunday
    }

  @staticmethod
  def _parse_time_range(time_range: str) -> tuple[datetime.time, datetime.time]:
    """Parse a time range string (e.g., '06:00-07:00') into start and end times"""
    start_str, end_str = time_range.split("-")
    start_time = datetime.strptime(start_str, "%H:%M").time()
    end_time = datetime.strptime(end_str, "%H:%M").time()
    return start_time, end_time

  @classmethod
  def get_current_activity(cls):
    current_datetime = datetime.now()
    mumbai_time = datetime.now(ZoneInfo("Asia/Kolkata"))
    current_time= mumbai_time.time()
    current_day = current_datetime.weekday()
    schedule = cls.SCHEDULES.get(current_day, {})

    for time_range, activity in schedule.items():
      start_time, end_time = cls._parse_time_range(time_range)
      if start_time > end_time:
        if current_time >= start_time or current_time <= end_time:
            return activity
      else:
        if start_time <= current_time <= end_time:
            return activity
    return None
