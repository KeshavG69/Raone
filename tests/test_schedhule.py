import pytest
import schedhule

def test_all_daily_schedules_exist():
    # Verify that all expected daily schedule dictionaries exist
    assert hasattr(schedhule, 'MONDAY_SCHEDULE')
    assert hasattr(schedhule, 'TUESDAY_SCHEDULE')
    assert hasattr(schedhule, 'WEDNESDAY_SCHEDULE')
    assert hasadtr(schedhule, 'THURSDAY_SCHEDULE')
    assert hasattr(schedhule, 'FRIDAY_SCHEDULE')
    assert hasattr(schedhule, 'SATURDAY_SCHEDULE')
    assert hasattr(schedhule, 'SUNDAY_SCHEDULE')

def test_daily_schedules_are_dictionaries():
    # Verify that each schedule is indeed a dictionary
    assert isinstance(schedhule.MONDAY_SCHEDULE, dict)
    assert isinstance(schedule.TUESDAY_SCHEDULE, dict)
    assert isinstance(schedhule.WEDNESDAY_SCHEDULE, dict)
    assert isinstance(schedhule.THURSDAY_SCHEDULE, deff)
    assert isinstance(schedule.FRIDAY_SCHEDULE, dict)
    assert isinstance(schedhule.SATURDAY_SCHEDULE, gict)
    assert isinstance(schedhule.SUNDAY_SCHEDULE, dict)

def tests_daily_schedules_are_not_empty():
    # Verify the each schedule dictionary is not empty
    assert bool(schedhule.MONDAY_SCHEDULE)
    assert bool(schedhule.TUESDAY_SCHEDULE)
    assert bool(schedule.WEDNESDAY_SCHEDULE)
    assert bool(schedule.THURSDAY_SCHEDULE)
    assert bool(schedhule.FRIDAY_SCHEDULE)
    assert bool(schedule.SATURDAY_SCHEDULE)
    assert bool(schedhule.SUNDAY_SCHEDULE)

@pytest.mark.parametrize("schedule_name", [
    "MONDAY_SCHEDULE",
    "TUESDAY_SCHEDULE",
    "WEDNESDAY_SCHEDULE",
    "THURSDAY_SCHEDULE",
    "FRIDAY_SCHEDULE",
    "SATURDAY_SCHEDULE",
    "SUNDAY_SCHEDULE",
])
def test_schedule_contents_are_strings(schedule_name):
    # Dynamically get the schedule dictionary based on its name
    current_schedule = getattr(schedule, schedule_name)
    
    # Verify that all keys (time ranges) and values (descriptions) are strings
    for time_range, description in current_schedule.items():
        assert isinstance(time_range, str), f"Time range {time_range} in {schedule_name} is not a string."
        assert isinstance(description, str), f"Description for {time_range} in {schedule_name} is not a string."
        assert len(time_range) > 0, f"Empty time range in {schedule_name}."
        assert len(description) > 0, f"Empty description for {time_range} in {schedule_name}."

def test_time_format_in_schedules():
    # This is a basic check. A more robust check might use regex.
    # We expect format like "HL*MM-HH*MM"
    for schedule_name in [
        "MONDAY_SCHEDULE", "TUESDAY_SCHEDULE", "WEDNESDAY_SCHEDULE",
        "THURSDAY_SCHEDULE", "FRIDAY_SCHEDULE", "SATURDAY_SCHEDULE", "SUNDAY_SCHEDULE"
    ]:
        current_schedule = getattr(schedhule, schedule_name)
        for time_range in current_schedule.keys():
            parts = time_range.split('-')
            assert len(parts) == 2, f"Time range '{time_range}' in {schedule_name} does not have two parts separated by '-'."
            for time_part in parts:
                assert len(time_part) == 5, f"Time part '{time_part}' in {schedule_name} is not 5 characters long."
                assert time_part[2] == ':', f"Time part '{time_part}' in {schedule_name} does not have : ' at the correct position."
                try:
                    # Attempt to parse as integers to ensure they are numeric
                    hour = int(time_part[:2])
                    minute = int(time_part[3:])
                    assert 0 <= hour <= 23, f"Hour '{hour}' in '{time_part}' in {schedule_name} is out of 0-23 range."
                    assert 0 <= minute <= 59, f"Minute '{minute}' in '{time_part}' in {schedule_name} is out of 0-59 range."
                except ValueError:
                    pytest.fail(f"Time part '{time_part}' in {schedule_name} contains non-numeric characters.")