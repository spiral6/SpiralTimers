import datetime
import json
import re
from enum import Enum

class Timer:
    name = ""
    weekday = -1
    hour = -1
    minute = -1
    reset = None
    delta = None

    def __init__(self, name, weekday, hour, minute):
        self.name = name
        self.weekday = weekday
        self.hour = hour
        self.minute = minute
        
    def determine_reset(self):
        current_time = datetime.datetime.now()
        reset_day_offset = self.weekday - current_time.weekday() # 1 = Tuesday
        if reset_day_offset < 0:
            reset_day_offset += 7
        reset_hour_offset = self.hour - current_time.time().hour
        reset_min_offset = self.minute - current_time.time().minute
        reset_sec_offset = 0 - current_time.time().second
        reset_time = current_time + datetime.timedelta(days=reset_day_offset, hours=reset_hour_offset, minutes=reset_min_offset, seconds=reset_sec_offset)

        self.reset = reset_time
        self.delta = current_time - reset_time
        if self.delta.total_seconds() >= 0:
            reset_time = current_time + datetime.timedelta(days=reset_day_offset + 7, hours=reset_hour_offset, minutes=reset_min_offset, seconds=reset_sec_offset)
            self.delta = current_time - reset_time
            self.reset = reset_time

        reset_str = reset_time.strftime("%A %B %d, %Y %I:%M:%S %p")
        return reset_str
    
class Weekday(Enum):
    Monday = 0
    Tuesday = 1
    Wednesday = 2
    Thursday = 3
    Friday = 4
    Saturday = 5
    Sunday = 6