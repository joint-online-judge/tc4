from os import listdir, path, rmdir
import re
from shutil import move

TIME_RE = re.compile(r'([0-9]+(?:\.[0-9]*)?)([mun]?)s?')
TIME_UNITS = {'': 1000000000, 'm': 1000000, 'u': 1000, 'n': 1}
MEMORY_RE = re.compile(r'([0-9]+(?:\.[0-9]*)?)([kmg]?)b?')
MEMORY_UNITS = {'': 1, 'k': 1024, 'm': 1048576, 'g': 1073741824}


def parse_time_ns(time_str):
    match = TIME_RE.fullmatch(time_str)
    if not match:
        raise ValueError(time_str, 'error parsing time')
    return int(float(match.group(1)) * TIME_UNITS[match.group(2)])


def parse_memory_bytes(memory_str):
    match = MEMORY_RE.fullmatch(memory_str)
    if not match:
        raise ValueError(memory_str, 'error parsing memory')
    return int(float(match.group(1)) * MEMORY_UNITS[match.group(2)])


def movechilden(src, dst):
    """Recursively move all children of a directory tree.

    Requires both src and dest to exist
    Replace files with same names in dest

    :param src: the source directory
    :param dst: the destination directory

    """
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(d):
            movechilden(s, d)
            rmdir(s)
        else:
            move(s, d)
