import datetime 
from math import floor
import shlex
import copy
class Schedule:
    def __init__(self, times, names):
        self.times = times.split()
        for i in range(len(self.times)):
            self.times[i] = self.times[i].split('-')
        self.times_pristine = copy.deepcopy(self.times)
        self.names = names
        self.names = shlex.split(self.names)

    def __getitem__(self, key):
        idx = self.names.index(key)
        return self.times[idx]

    def pristine(self):
        self.times = copy.deepcopy(self.times_pristine)

    def flex_next_sleep(self, amount):
        for i in range(len(self[self.next()])):
            time = self[self.next()][i]
            flex = datetime.timedelta(minutes=amount)
            time = datetime.datetime.strptime(time, '%H:%M') 
            time += flex
            time = datetime.datetime.strftime(time, '%H:%M')
            self.times[self.names.index(self.next())][i] = time

    def next(self):
        now = datetime.datetime.now()
        next_sleep = []
        for i in range(0, len(self.times)):
            next_sleep.append(datetime.datetime.strptime(self.times[i][0],
                "%H:%M"))
            next_sleep[i] = next_sleep[i].replace(year=now.year, month=now.month, day=now.day)
            if next_sleep[i] < now:
                next_sleep[i] += datetime.timedelta(days=1)
        ns = min(next_sleep, key=lambda x: x - now)
        return self.names[next_sleep.index(ns)]

    def remaining(self):
        now = datetime.datetime.now()
        next_sleep = []
        for i in range(0, len(self.times)):
            next_sleep.append(datetime.datetime.strptime(self.times[i][0], "%H:%M"))
            next_sleep[i] = next_sleep[i].replace(year=now.year, month=now.month, day=now.day)
            if next_sleep[i] < now:
                next_sleep[i] += datetime.timedelta(days=1)
        ns = min(next_sleep, key=lambda x: x - now)
        remaining = (ns - now).seconds
        hours = remaining // 3600
        minutes = remaining // 60 - 60 * hours
        seconds = floor(remaining) - 60 * minutes - 3600 * hours
        timefmt = str(hours) + ':' + str(minutes).zfill(2) + ':' + str(seconds).zfill(2)
        return timefmt

    def prettify(self):
        times_pretty = ''
        for i in range(0,len(self.times)):
            times_pretty += self.times[i][0]
            times_pretty += '-'
            times_pretty += self.times[i][1]
            if i is not len(self.times) - 1:
                times_pretty += ' '
        return times_pretty

    def isAsleep(self):
        now = datetime.datetime.now()
        sleeps = []
        wakes = []
        day = datetime.timedelta(days=1)
        for timerange in self.times:
            sleeps.append(datetime.datetime.strptime(timerange[0],
                "%H:%M").replace(year=now.year, month=now.month, day=now.day))
            wakes.append(datetime.datetime.strptime(timerange[1],
                "%H:%M").replace(year=now.year, month=now.month, day=now.day))
            if sleeps[-1] - datetime.timedelta(minutes=10) > now:
                sleeps[-1] -= day
            if wakes[-1] - sleeps[-1] > day:
                wakes[-1] -= day
            if sleeps[-1] > wakes[-1]:
                wakes[-1] += day
        for i in range(0, len(sleeps)):
            if sleeps[i] - datetime.timedelta(minutes=10) < now < wakes[i]:
                #print(now)
                #print(sleeps)
                #print(wakes)
                return True
        
        return False

        


