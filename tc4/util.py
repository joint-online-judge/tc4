from os import listdir, path, rmdir
from shutil import move


def movechilden(src, dst):
    """Recursively move all children of a directory tree.

    Requires both src and dest to exist
    :param src: the source directory
    :param dst: the destination directory

    """
    for item in listdir(src):
        s = path.join(src, item)
        d = path.join(dst, item)
        if path.isdir(d):
            movechilden(s, d)
        else:
            move(s, d)
    rmdir(src)
