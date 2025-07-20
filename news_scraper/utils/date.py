import re
import jdatetime

def parse_persian_datetime(raw_text):
    raw_text = raw_text.replace('\u200c', ' ').strip()

    pattern = r"(?P<weekday>\S+\s*\S*)\s+(?P<day>\d{1,2})\s+(?P<month>\S+)\s+(?P<year>\d{4})\s*-\s*(?P<hour>\d{1,2}):(?P<minute>\d{2})"
    match = re.match(pattern, raw_text)
    if not match:
        raise ValueError(f"Pattern mismatch: can't parse `{raw_text}`")

    groups = match.groupdict()
    day = int(groups["day"])
    month_name = groups["month"]
    year = int(groups["year"])
    hour = int(groups["hour"])
    minute = int(groups["minute"])

    month_map = {
        "فروردین": 1, "اردیبهشت": 2, "خرداد": 3,
        "تیر": 4, "مرداد": 5, "شهریور": 6,
        "مهر": 7, "آبان": 8, "آذر": 9,
        "دی": 10, "بهمن": 11, "اسفند": 12
    }

    month = month_map.get(month_name)
    if not month:
        raise ValueError(f"Unknown Persian month: `{month_name}`")

    try:
        jdate = jdatetime.datetime(year, month, day, hour, minute)
        return jdate.togregorian()
    except ValueError as e:
        raise ValueError(f"Invalid Jalali date: {e}")
