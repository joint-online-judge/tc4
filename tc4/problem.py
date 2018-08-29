from os import path, makedirs
from shutil import copytree, rmtree, move
from tempfile import mkdtemp
from zipfile import ZipFile

from tc4.util import movechilden


class Problem:
    def __init__(self, file):
        self.zip_file = ZipFile(file)
        # make case insensitive in tc4
        self.canonical_dict = dict((name.lower(), name) for name in self.zip_file.namelist())
        self.extract_dir = mkdtemp(prefix='tc4.zipfile.')

    def __del__(self):
        rmtree(self.extract_dir)

    def open(self, name):
        try:
            return self.zip_file.open(self.canonical_dict[name.lower()])
        except KeyError:
            raise FileNotFoundError(name) from None

    def extract(self, name, dest):
        file_found = False
        head, tail = path.split(name)

        if not name.endswith('/'):
            if name.lower() in self.canonical_dict:
                # single file
                file_found = True
                self.zip_file.extract(self.canonical_dict[name.lower()], path=self.extract_dir)
            else:
                head = name + '/'
                dest = path.join(dest, tail)
        else:
            head += '/'

        if not file_found:
            if head.lower() in self.canonical_dict:
                # directory
                file_found = True
                for compressed_file in self.canonical_dict:
                    if compressed_file.startswith(head.lower()):
                        self.zip_file.extract(self.canonical_dict[compressed_file], path=self.extract_dir)

        if file_found:
            if not path.isdir(dest):
                makedirs(dest)
            movechilden(path.join(self.extract_dir, head), dest)

        if not file_found:
            raise FileNotFoundError(name) from None


def load_problem(file):
    return Problem(file)


# test
if __name__ == '__main__':
    problem = load_problem('example/test.zip')
    print(problem.canonical_dict)
    problem.extract('compile/test/recursive.h', 'example/folder')
