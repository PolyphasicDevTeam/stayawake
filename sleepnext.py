import datetime 
from math import floor
def next(schedule, names):
    now = datetime.datetime.now()
    next_sleep = []
    for i in range(0, len(schedule)):
        next_sleep.append(datetime.datetime.strptime(schedule[i][0], "%H:%M"))
        next_sleep[i] = next_sleep[i].replace(year=now.year, month=now.month, day=now.day)
        if next_sleep[i] < now:
            next_sleep[i] += datetime.timedelta(days=1)
    ns = min(next_sleep, key=lambda x: x - now)
    return names[next_sleep.index(ns)]

def time_remaining(schedule):
    now = datetime.datetime.now()
    next_sleep = []
    for i in range(0, len(schedule)):
        next_sleep.append(datetime.datetime.strptime(schedule[i][0], "%H:%M"))
        next_sleep[i] = next_sleep[i].replace(year=now.year, month=now.month, day=now.day)
        if next_sleep[i] < now:
            next_sleep[i] += datetime.timedelta(days=1)
    ns = min(next_sleep, key=lambda x: x - now)
    remaining = (ns - now).seconds
    hours = floor(remaining/3600)
    minutes = floor(remaining / 60) - 60 * hours
    seconds = floor(remaining) - 60 * minutes - 3600 * hours
    timefmt = str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
    return timefmt 
