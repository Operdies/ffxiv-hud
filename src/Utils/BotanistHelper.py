from time import time, sleep
from datetime import datetime, timedelta
from playsound import playsound
import threading
import re
import os

SCHEDULE_FILE = 'schedule.txt'


def run_in_thread(fn):
    def run(*k, **kw):
        t = threading.Thread(target=fn, args=k, kwargs=kw)
        t.start()
        return t  # <-- this is new!

    return run


class BotanistHelper:
    def update_schedule(self, force=False):
        try:
            comment_re = r'(^[^#]*)'  # reads all characters until a # is encountered
            change_time = os.stat(SCHEDULE_FILE).st_mtime
            if change_time != self.schedule_changed or force:
                events = []
                with open(SCHEDULE_FILE, 'r', encoding='ascii') as h:
                    lines = h.readlines()
                lines = [re.findall(comment_re, line)[0] for line in lines]
                lines = [line for line in lines if len(line) > 1]
                for line in lines:
                    try:
                        times, item, zone, slot = [v.strip() for v in line.split(':')]
                    except ValueError:
                        continue
                    times = [int(t.strip()) for t in times.split(',')]
                    for time in times:
                        events += [(time, item, zone, slot)]

                self.schedule_changed = change_time
                events.sort(key=lambda x: x[0])
                return events
        except:  # retry next tick because
            pass

        return self.events

    def __init__(self, unix_time, dt, ratio):
        self.playing = False  # whether a sound is playing. prevents overlapping sounds
        self.unix_time = unix_time  # real life timestamp when measurement started
        self.dt = dt  # ingame datetime when measurement started
        self.ratio = ratio  # real seconds per ingame minute
        self.schedule_changed = os.stat(SCHEDULE_FILE).st_mtime
        self.events = self.update_schedule(force=True)

    @run_in_thread  # non-blocking calls, yo
    def play_alert(self):
        if not self.playing:
            self.playing = True
            playsound('alert.wav')
            self.playing = False

    def get_et(self):
        elapsed = time() - self.unix_time
        seconds = int(60 * elapsed / self.ratio)
        current = self.dt + timedelta(seconds=seconds)
        return current

    def report(self):
        self.events = self.update_schedule()
        current = self.get_et()
        prior_area = self.events[-1][-1]
        for t, item, area, slot in self.events:
            if t > current.hour:
                next_event = self.time_to_time(t)
                break
            prior_area = slot
        else:
            t, item, area, slot = self.events[0]
            next_event = self.time_to_time(t)

        # prior_area = slot

        if "00:30" in next_event:
            self.play_alert()

        time_text = '{} {}'.format(t % 12 if t % 12 is not 0 else 12, 'AM' if t < 12 else 'PM')
        # event_string = " - Next event in {next_event} ({area} [{item}] - {tt}) - Current slot: {slot}  ".format(
        event_string = " - {area} [{item}] - {tt} in {next_event} (slot {slot}) ".format(
            next_event=next_event, area=area, item=item, tt=time_text, slot=prior_area)

        result = ' ' + current.strftime('%I:%M %p') + event_string
        if self.highlight:
            result = '>>' + result + '<<'

        return result

    def time_to_time(self, hour):
        current = self.get_et()
        h, m, s = current.hour, current.minute, current.second
        time_of_day = timedelta(hours=h, minutes=m, seconds=s)
        e_timespan = timedelta(hours=hour) - time_of_day if hour > current.hour else timedelta(days=1,
                                                                                               hours=hour) - time_of_day

        seconds = e_timespan.total_seconds()

        seconds /= 60 / self.ratio
        minutes = str(int(seconds / 60))
        seconds = str(int(seconds) % 60)

        fix = lambda x: '0' + x if len(x) is 1 else x

        minutes = fix(minutes)
        seconds = fix(seconds)
        return '{}:{}'.format(minutes, seconds)
