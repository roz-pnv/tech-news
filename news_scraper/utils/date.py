import re
import jdatetime

def parse_persian_datetime(raw_text):
    raw_text = raw_text.strip()

    match = re.match(r"(\w+)\s+(\d{1,2})\s+(\w+)\s+(\d{4})\s*-\s*(\d{1,2}):(\d{2})", raw_text)
    if not match:
        return None

    weekday_name, day, month_name, year, hour, minute = match.groups()

    month_map = {
        "فروردین": 1, "اردیبهشت": 2, "خرداد": 3,
        "تیر": 4, "مرداد": 5, "شهریور": 6,
        "مهر": 7, "آبان": 8, "آذر": 9,
        "دی": 10, "بهمن": 11, "اسفند": 12
    }

    month = month_map.get(month_name)
    if not month:
        return None

    jdate = jdatetime.datetime(int(year), month, int(day), int(hour), int(minute))
    return jdate.togregorian()
