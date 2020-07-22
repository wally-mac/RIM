import sys
import time
import gc
import sys
import glob
import shutil
import os
from math import cos, sin, asin, sqrt, radians
from lib.loghelper import Logger

# Set if this environment variable is set don't show any UI
NO_UI = os.environ.get('NO_UI') is not None


def safe_makedirs(dir_create_path):
    """safely, recursively make a directory

    Arguments:
        dir_create_path {[type]} -- [description]
    """
    log = Logger("MakeDir")

    # Safety check on path lengths
    if len(dir_create_path) < 5 or len(dir_create_path.split(os.path.sep)) <= 2:
        raise Exception('Invalid path: {}'.format(dir_create_path))

    if os.path.exists(dir_create_path) and os.path.isfile(dir_create_path):
        raise Exception('Can\'t create directory if there is a file of the same name: {}'.format(dir_create_path))

    if not os.path.exists(dir_create_path):
        try:
            log.info('Folder not found. Creating: {}'.format(dir_create_path))
            os.makedirs(dir_create_path)
        except Exception as e:
            # Possible that something else made the folder while we were trying
            if not os.path.exists(dir_create_path):
                log.error('Could not create folder: {}'.format(dir_create_path))
                raise e


def sizeof_fmt(num, suffix='B'):
    """Format bytesize properly

    Arguments:
        num {[type]} -- [description]

    Keyword Arguments:
        suffix {str} -- [description] (default: {'B'})

    Returns:
        [type] -- [description]
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def calc_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

# class Spinner:

#     def __init__(self, text, timer=500):
#         self.lastupdate = time.time()
#         self.timer = timer
#         self.text = text

#     def output(self):
#         elapsed_time = time.time() - self.lastupdate
#         if (elapsed_time > self.timer):
#             sys.stdout.write("\r[{}{}]    {} / {}    {}     ".format('=' * done, ' ' * (50 - done), sizeof_fmt(self.byte_progress), sizeof_fmt(self.byte_total), self.text))
#             sys.stdout.flush()


class Timer:
    def __init__(self, name, logger=Logger("TIMER"), useMs=False, timer=500):
        self.useMs = useMs
        self.logger = logger
        self.timer = 20000 if NO_UI else timer
        self.start = time.time()
        self.name = name
        self.lastupdate = time.time()
        self.visible = False
        # average
        self.total = 0
        self.ticks = 0

    def reset(self):
        self.start = time.time()

    def tick(self):
        self.total += time.time() - self.start
        self.ticks += 1
        self.start = time.time()

    def print(self, midStr=None, useMs=False):
        if NO_UI:
            return
        if self.visible:
            self.erase()
        middleStr = "::{}".format(midStr) if midStr else ""
        if self.ticks > 0:
            avg = self.total / self.ticks
            if useMs or self.useMs:
                avg = avg * 1000
            self.logger.debug("{}{}:: Count: {:,}, Total Time: {:f}s, Average: {:f}{}"
                              .format(self.name, middleStr, self.ticks, self.total, avg, "ms" if self.useMs else "s"))
        else:
            ellapsed = time.time() - self.start
            if useMs or self.useMs:
                ellapsed = ellapsed * 1000
            self.logger.debug("{}{}::{:f}{}".format(self.name, middleStr, ellapsed, "ms" if self.useMs else "s"))

    def erase(self):
        if self.visible:
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")  # wipe line
        self.visible = False

    def progprint(self, midStr=None):
        if NO_UI:
            return
        middleStr = "::{}".format(midStr) if midStr else ""
        since_last = 1000 * (time.time() - self.lastupdate)
        if self.ticks > 0 and since_last > self.timer:
            self.erase()
            avg = self.total / self.ticks
            if self.useMs:
                avg = avg * 1000
            tSize = shutil.get_terminal_size((80, 20))
            self.lastupdate = time.time()
            writestr = "\rAVG_TIMER::{}{}:: Count: {:,}, Total Time: {:f}s, Average: {:f}{}     \n".format(self.name, middleStr, self.ticks, self.total, avg, "ms" if self.useMs else "s")
            if len(writestr) > tSize.columns - 1:
                writestr = writestr[0:tSize.columns - 4] + '   \n'
            sys.stdout.write(writestr)
            sys.stdout.flush()
            self.visible = True


class ProgressBar:

    def __init__(self, total, char_size=50, text=None, timer=500, byteFormat=False):
        self.log = Logger('ProgressBar')
        self.char_size = char_size
        self.text = text
        self.byteFormat = byteFormat
        self.start_time = None
        self.lastupdate = time.time()
        self.timer = 20000 if NO_UI else timer
        self.progress = 0
        self.visible = False
        self.total = total

    def update(self, progress):
        self.progress = progress
        self.output()

    def erase(self):
        if NO_UI:
            return
        if self.visible:
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")  # wipe line
        self.visible = False

    def finish(self):
        if self.byteFormat:
            writestr = "Finished: {}    {}     \n".format(sizeof_fmt(self.total), self.text)
        else:
            writestr = "Finished: {:,}    {}     \n".format(self.total, self.text)
        sys.stdout.write(writestr)
        sys.stdout.flush()

    def output(self):
        first_time = False
        if self.start_time is None:
            first_time = True
            self.start_time = time.time()
        elapsed_time = 1000 * (time.time() - self.lastupdate)
        # For NO_UI we still want a keepalive signal but we don't want the quick-update progress bars
        if NO_UI:
            if first_time or elapsed_time > self.timer:
                self.lastupdate = time.time()
                writestr = ""
                time_since_begun = int(time.time() - self.start_time)
                if self.byteFormat:
                    writestr = "        PROGRESS: {} / {}    {}     Ellapsed: {:n}s\n".format(sizeof_fmt(self.progress), sizeof_fmt(self.total), self.text, time_since_begun)
                else:
                    pct_done = int(100 * (self.progress / self.total))
                    writestr = "        PROGRESS: {:,} / {:,}  ({}%)  {}     Ellapsed: {:n}s\n".format(self.progress, self.total, pct_done, self.text, time_since_begun)
                sys.stdout.write(writestr)
                sys.stdout.flush()
            return
        if first_time or elapsed_time > self.timer:
            tSize = shutil.get_terminal_size((80, 20))
            self.lastupdate = time.time()
            done = 0
            if self.total > 0:
                done = int(50 * self.progress / self.total)
            self.erase()
            writestr = ""
            if self.byteFormat:
                writestr = "\r[{}{}]    {} / {}    {}     \n".format('=' * done, ' ' * (50 - done), sizeof_fmt(self.progress), sizeof_fmt(self.total), self.text)
            else:
                writestr = "\r[{}{}]    {:,} / {:,}    {}     \n".format('=' * done, ' ' * (50 - done), self.progress, self.total, self.text)

            if len(writestr) > tSize.columns - 1:
                writestr = writestr[0:tSize.columns - 4] + '   \n'

            sys.stdout.write(writestr)
            sys.stdout.flush()
            self.visible = True


def get_obj_size(obj):
    """Generic function to get the byte-size of a variable

    Arguments:
        obj {[type]} -- [description]

    Returns:
        [type] -- [description]
    """
    marked = {id(obj)}
    obj_q = [obj]
    sz = 0

    while obj_q:
        sz += sum(map(sys.getsizeof, obj_q))

        # Lookup all the object referred to by the object in obj_q.
        # See: https://docs.python.org/3.7/library/gc.html#gc.get_referents
        all_refr = ((id(o), o) for o in gc.get_referents(*obj_q))

        # Filter object that are already marked.
        # Using dict notation will prevent repeated objects.
        new_refr = {o_id: o for o_id, o in all_refr if o_id not in marked and not isinstance(o, type)}

        # The new obj_q will be the ones that were not marked,
        # and we will update marked with their ids so we will
        # not traverse them again.
        obj_q = new_refr.values()
        marked.update(new_refr.keys())

    return sz


def parse_metadata(arg_string):

    meta = {}
    try:
        if arg_string:
            for kvp in arg_string.split(','):
                key_value = kvp.split('=')
                clean_key = key_value[0].strip()
                clean_value = key_value[1].strip()
                if len(clean_key) < 1:
                    raise Exception('Empty key')
                if len(clean_value) < 1:
                    raise Exception('Empty value')
                if clean_key in meta:
                    raise Exception('Duplicate metadata key')

                meta[clean_key] = clean_value
    except Exception as ex:
        raise Exception('Error parsing command line metadata: {}'.format(arg_string))

    return meta
